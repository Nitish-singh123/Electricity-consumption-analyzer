"""
Electricity Consumption Analyzer - TCP client.

Reads a CSV dataset of electricity consumption records, sends them to the
analysis server over TCP and prints the final analysis report.

Typical use (server running in another terminal):

    python client.py                # test case 1: dataset.csv
    python client.py --testcase 2   # test case 2: dataset_high.csv
    python client.py --testcase 3   # test case 3: dataset_edge.csv

Use `python testcases.py <1|2|3|all>` to run a test case end to end without
starting the server manually.
"""

import argparse
import csv
import json
import os
import socket
import sys
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 65432
CONNECTION_RETRIES = 8
RETRY_DELAY = 0.4

# Test case number -> (title, dataset file)
TESTCASES = {
    1: ("Normal dataset", "dataset.csv"),
    2: ("High-usage dataset", "dataset_high.csv"),
    3: ("Edge-case dataset", "dataset_edge.csv"),
}


def resolve_dataset(name):
    """Find a dataset regardless of the current working directory.

    An absolute path is used as-is; a path that exists relative to the current
    directory is kept; otherwise the name is resolved next to this script.
    """
    if os.path.isabs(name) or os.path.exists(name):
        return name
    return os.path.join(BASE_DIR, name)


def load_dataset(path):
    """Read a CSV dataset and return a list of typed record dictionaries."""
    with open(resolve_dataset(path), newline="", encoding="utf-8") as handle:
        records = []
        for row in csv.DictReader(handle):
            records.append(
                {
                    "record_id": int(row["record_id"]),
                    "customer_id": row["customer_id"].strip(),
                    "customer_name": row["customer_name"].strip(),
                    "date": row["date"].strip(),
                    "day_index": int(row["day_index"]),
                    "peak_units": float(row["peak_units"]),
                    "offpeak_units": float(row["offpeak_units"]),
                }
            )
    return records


def send_records(host, port, records, timeout=10.0):
    """Send the records over TCP and return the analysis dictionary.

    Retries briefly so the client still works if the server needs a moment to
    start.  Raises RuntimeError when the server cannot be reached or reports an
    error.
    """
    payload = (json.dumps(records) + "\n").encode("utf-8")
    buffer = b""

    for attempt in range(1, CONNECTION_RETRIES + 1):
        try:
            with socket.create_connection((host, port), timeout=timeout) as connection:
                connection.sendall(payload)
                buffer = b""
                while not buffer.endswith(b"\n"):
                    chunk = connection.recv(4096)
                    if not chunk:
                        break
                    buffer += chunk
            break
        except OSError as exc:
            if attempt == CONNECTION_RETRIES:
                raise RuntimeError(
                    "could not reach the server at %s:%d after %d attempts (%s)"
                    % (host, port, CONNECTION_RETRIES, exc)
                ) from exc
            time.sleep(RETRY_DELAY)

    response = json.loads(buffer.decode("utf-8"))
    if not response.get("ok"):
        raise RuntimeError("the server reported an error: %s" % response.get("error", "unknown"))
    return response["analysis"]


def number(value):
    """Compact formatting: 12.0 -> '12', 12.5 -> '12.5'."""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def print_report(analysis, title=None, stream=None):
    """Print the final analysis.  `title` labels the report (test case name)."""
    out = stream or sys.stdout

    def emit(text=""):
        print(text, file=out)

    def separator(text=""):
        line = "=" * 78 if not text else ("-" * 6 + " %s " % text).ljust(78, "-")[:78]
        emit(line)

    summary = analysis["summary"]
    budget = analysis["budget"]

    separator()
    emit(title or "ELECTRICITY CONSUMPTION ANALYZER - FINAL ANALYSIS")
    separator()
    emit("Records received  : %d" % analysis["records_received"])
    emit("Records analyzed  : %d   (invalid: %d)"
         % (analysis["records_analyzed"], analysis["records_invalid"]))
    emit("Customers         : %d" % summary["customers"])
    emit("Total units       : %s" % number(summary["total_units"]))
    emit("Total TOU bill    : Rs %s" % number(summary["total_tou_bill"]))
    emit("Avg units/record  : %s" % number(summary["average_units_per_record"]))

    separator("PER-CUSTOMER ANALYSIS (ranked by total units)")
    for customer in analysis["customers"]:
        emit("[%d] %s %s | %s units | TOU bill Rs %s | slab bill Rs %s"
             % (customer["rank"], customer["customer_id"], customer["customer_name"],
                number(customer["total_units"]), number(customer["tou_bill"]),
                number(customer["slab_bill"])))
        emit("    Daily units    : %s" % " -> ".join(number(u) for u in customer["daily_units"]))
        emit("    FSM path       : %s" % " -> ".join(customer["fsm_path"]))
        emit("    Final state    : %s" % customer["final_state"])
        emit("    Trend (SymPy)  : %s  =>  day %d prediction: %s units"
             % (customer["trend_equation"], customer["days"] + 1,
                number(customer["predicted_next_day_units"])))
        emit("    Recommendation : %s" % customer["recommendation"])
        emit()

    separator("HIGH-USAGE RECORDS (total units >= 20 per day)")
    high_usage = analysis["high_usage_records"]
    if high_usage:
        for record in high_usage:
            emit("  rec %-3d %s %s on %s : %s units (bill Rs %s)"
                 % (record["record_id"], record["customer_id"], record["customer_name"],
                    record["date"], number(record["total_units"]), number(record["tou_bill"])))
    else:
        emit("  none")
    emit()

    separator("BUDGET ADVICE (SymPy slab solve)")
    emit("  Monthly budget        : Rs %s" % number(budget["monthly_budget"]))
    emit("  Max units allowed     : %s units" % number(budget["max_units_allowed"]))
    emit("  Customers over budget : %s" % ", ".join(budget["customers_over_budget"]))
    separator()


def resolve_source(arguments):
    """Return (title, dataset) for the requested test case or dataset."""
    if arguments.testcase:
        case_title, dataset = TESTCASES[arguments.testcase]
        return "TEST CASE %d - %s (%s)" % (arguments.testcase, case_title.upper(), dataset), dataset
    return "ELECTRICITY CONSUMPTION ANALYZER - FINAL ANALYSIS", arguments.dataset


def main():
    parser = argparse.ArgumentParser(description="Electricity Consumption Analyzer - TCP client")
    parser.add_argument("--host", default=DEFAULT_HOST, help="server host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="server port (default: 65432)")
    parser.add_argument("--testcase", type=int, choices=sorted(TESTCASES),
                        help="run a prepared test case (1, 2 or 3)")
    parser.add_argument("--dataset", default="dataset.csv", help="CSV dataset (default: dataset.csv)")
    parser.add_argument("--verbose", action="store_true", help="show connection details")
    arguments = parser.parse_args()

    title, dataset = resolve_source(arguments)
    try:
        records = load_dataset(dataset)
    except (FileNotFoundError, OSError):
        raise SystemExit(
            "Cannot read the dataset '%s'.\n"
            "Use --testcase 1|2|3, or pass --dataset <path>, or run the client\n"
            "from the project folder (%s)." % (dataset, BASE_DIR)
        )
    if arguments.verbose:
        print("Loaded %d records from %s" % (len(records), dataset))
        print("Connecting to the server at %s:%d ..." % (arguments.host, arguments.port))

    try:
        analysis = send_records(arguments.host, arguments.port, records)
    except RuntimeError as exc:
        raise SystemExit("%s\nStart the server first in another terminal:\n    python server.py"
                         % exc)
    print_report(analysis, title=title)


if __name__ == "__main__":
    main()
