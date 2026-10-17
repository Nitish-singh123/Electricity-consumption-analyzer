"""
Electricity Consumption Analyzer - TCP server.

Receives electricity consumption records from the client over TCP and applies:

* a 4-state FSM over daily consumption bands,
* functional programming (map / filter / reduce / closures) for every
  transformation and aggregation,
* SymPy for the slab tariff model, the least-squares trend fit and the
  budget break-even solve.

Wire protocol: one newline-terminated JSON list in, one newline-terminated JSON
object out.  See README.md for setup and usage.
"""

import argparse
import json
import socket
from functools import reduce
from itertools import groupby

try:
    from sympy import Eq, Piecewise, solve, symbols
except ImportError:  # friendly message instead of a ModuleNotFoundError traceback
    raise SystemExit(
        "SymPy is not installed for this Python interpreter.\n"
        "Install it with:  pip install sympy\n"
        "(check you are using the same interpreter:  python -c \"import sys; print(sys.executable)\")"
    )

# --------------------------------------------------------------------------
# FSM: states, input bands and the complete transition table
# --------------------------------------------------------------------------
STATES = ("LOW", "MODERATE", "HIGH", "OVERLOAD")
INPUT_BANDS = ("LT10", "B10_19", "B20_29", "GE30")
BAND_TARGET = {"LT10": "LOW", "B10_19": "MODERATE", "B20_29": "HIGH", "GE30": "OVERLOAD"}

# (current state, input band) -> next state
TRANSITIONS = {(state, band): BAND_TARGET[band] for state in STATES for band in INPUT_BANDS}

RECOMMENDATIONS = {
    "LOW": "Normal usage - no action needed.",
    "MODERATE": "Moderate load - shift heavy appliances to off-peak hours.",
    "HIGH": "High load - review appliances, consider rooftop solar.",
    "OVERLOAD": "Overload detected - take immediate action to cut peak demand.",
}


def band(total_units):
    """Return the FSM input band for a daily consumption total."""
    if total_units < 10:
        return "LT10"
    if total_units < 20:
        return "B10_19"
    if total_units < 30:
        return "B20_29"
    return "GE30"


def fsm_next(state, total_units):
    """FSM transition function: (current state, input) -> next state."""
    return TRANSITIONS[(state, band(total_units))]


def walk_fsm(initial_state, unit_list):
    """Run a sequence of daily totals through the FSM and return the state path."""
    state = initial_state
    path = [state]
    for units in unit_list:
        state = fsm_next(state, units)
        path.append(state)
    return path


# --------------------------------------------------------------------------
# SymPy: symbolic tariff, trend fit and budget solve
# --------------------------------------------------------------------------
RATE1 = 3.0
RATE2 = 5.0
SLAB_LIMIT = 50
MONTHLY_BUDGET = 500.0

x = symbols("x")

# bill(x) = 3x for x <= 50 and 3*50 + 5(x - 50) for x > 50
bill_expr = Piecewise(
    (RATE1 * x, x <= SLAB_LIMIT),
    (RATE1 * SLAB_LIMIT + RATE2 * (x - SLAB_LIMIT), x > SLAB_LIMIT),
)


def bill_amount(total_units):
    """Evaluate the symbolic slab tariff at a concrete consumption value."""
    return float(bill_expr.subs(x, total_units).evalf())


def fit_trend(day_totals):
    """Fit y = a*x + b to daily totals by solving the normal equations with SymPy.

    day_totals[0] belongs to day 1.  Returns the pair (a, b).
    """
    n = len(day_totals)
    days = list(range(1, n + 1))
    values = [float(v) for v in day_totals]
    sx, sy = sum(days), sum(values)
    sxx = sum(day * day for day in days)
    sxy = sum(day * value for day, value in zip(days, values))

    a, b = symbols("a b")
    solution = solve([Eq(sxx * a + sx * b, sxy), Eq(sx * a + n * b, sy)], (a, b), dict=True)[0]
    return float(solution[a]), float(solution[b])


def predict_day(a, b, day):
    """Predict consumption for a future day from the fitted trend line."""
    return round(a * day + b, 2)


def budget_units(budget):
    """Solve bill(x) = budget symbolically and return the affordable units.

    Each slab branch is solved separately and only the root inside its own
    domain is kept.  Returns None when no branch yields a valid root.
    """
    branches = (
        (RATE1 * x, lambda value: value <= SLAB_LIMIT),
        (RATE1 * SLAB_LIMIT + RATE2 * (x - SLAB_LIMIT), lambda value: value > SLAB_LIMIT),
    )
    solutions = []
    for expression, in_domain in branches:
        for root in solve(Eq(expression, budget), x):
            value = float(root)
            if in_domain(value):
                solutions.append(value)
    return round(max(solutions), 2) if solutions else None


# --------------------------------------------------------------------------
# Functional pipeline
# --------------------------------------------------------------------------
HIGH_THRESHOLD = 20.0


def make_bill_calculator(peak_rate=4.0, offpeak_rate=2.0):
    """Higher-order function returning a time-of-use bill calculator closure."""

    def calculate(peak_units, offpeak_units):
        return round(peak_units * peak_rate + offpeak_units * offpeak_rate, 2)

    calculate.peak_rate = peak_rate
    calculate.offpeak_rate = offpeak_rate
    return calculate


TOU_BILL = make_bill_calculator(4.0, 2.0)


def is_valid(record):
    """True when both unit readings are present and non-negative."""
    try:
        return record["peak_units"] >= 0 and record["offpeak_units"] >= 0
    except (KeyError, TypeError):
        return False


def enrich(record):
    """map step: add total units and the time-of-use bill to a record."""
    total = record["peak_units"] + record["offpeak_units"]
    enriched = dict(record)
    enriched["total_units"] = round(total, 2)
    enriched["tou_bill"] = TOU_BILL(record["peak_units"], record["offpeak_units"])
    return enriched


def customer_summary(records):
    """Analyse the records of a single consumer (FSM path, totals, trend)."""
    ordered = sorted(records, key=lambda item: item["day_index"])
    units = [item["total_units"] for item in ordered]
    path = walk_fsm("LOW", units)

    total_units = reduce(lambda acc, item: acc + item["total_units"], ordered, 0)
    total_bill = round(reduce(lambda acc, item: acc + item["tou_bill"], ordered, 0), 2)

    if len(units) >= 2:
        a_value, b_value = fit_trend(units)
    else:
        a_value, b_value = 0.0, units[0] if units else 0.0

    final_state = path[-1]
    return {
        "customer_id": ordered[0]["customer_id"],
        "customer_name": ordered[0]["customer_name"],
        "days": len(ordered),
        "daily_units": units,
        "fsm_path": path,
        "final_state": final_state,
        "recommendation": RECOMMENDATIONS[final_state],
        "total_units": round(total_units, 2),
        "tou_bill": total_bill,
        "slab_bill": bill_amount(total_units),
        "trend_a": round(a_value, 4),
        "trend_b": round(b_value, 4),
        "trend_equation": "y = %s%.4fx %s %.4f"
        % ("-" if a_value < 0 else "", abs(a_value), "+" if b_value >= 0 else "-", abs(b_value)),
        "predicted_next_day_units": predict_day(a_value, b_value, len(units) + 1),
    }


def analyze_records(records):
    """Run the complete analysis and return a JSON-serialisable result.

    Functional programming concepts used:
      map                    - enrich() builds the billing dictionaries
      filter                 - valid records and high-usage records
      reduce                 - grand totals
      lambda                 - inline keys and accumulators
      higher-order function   - make_bill_calculator() returns a closure
    """
    valid = list(filter(is_valid, records))
    invalid = list(filter(lambda item: not is_valid(item), records))

    billed = list(map(enrich, valid))
    high_usage = list(filter(lambda item: item["total_units"] >= HIGH_THRESHOLD, billed))

    grand_units = reduce(lambda acc, item: acc + item["total_units"], billed, 0)
    grand_bill = round(reduce(lambda acc, item: acc + item["tou_bill"], billed, 0), 2)
    average_units = round(grand_units / len(billed), 2) if billed else 0.0

    ordered = sorted(billed, key=lambda item: (item["customer_id"], item["day_index"]))
    summaries = [
        customer_summary(list(group))
        for _, group in groupby(ordered, key=lambda item: item["customer_id"])
    ]
    ranked = sorted(summaries, key=lambda customer: customer["total_units"], reverse=True)
    for position, customer in enumerate(ranked, start=1):
        customer["rank"] = position

    over_budget = [
        customer["customer_id"]
        for customer in ranked
        if bill_amount(customer["total_units"]) > MONTHLY_BUDGET
    ]

    return {
        "records_received": len(records),
        "records_analyzed": len(billed),
        "records_invalid": len(invalid),
        "invalid_records": invalid,
        "billed_records": billed,
        "high_usage_records": high_usage,
        "customers": ranked,
        "summary": {
            "customers": len(ranked),
            "total_units": round(grand_units, 2),
            "total_tou_bill": grand_bill,
            "average_units_per_record": average_units,
        },
        "budget": {
            "monthly_budget": MONTHLY_BUDGET,
            "max_units_allowed": budget_units(MONTHLY_BUDGET),
            "customers_over_budget": over_budget or ["none"],
        },
    }


# --------------------------------------------------------------------------
# TCP server
# --------------------------------------------------------------------------
MAX_MESSAGE = 10 * 1024 * 1024


def port_in_use(host, port):
    """True when something already accepts connections on host:port.

    Prevents a silent double bind: on Windows SO_REUSEADDR would otherwise let
    a second server start and leave clients talking to stale code.
    """
    if port == 0:
        return False
    probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    probe.settimeout(0.5)
    try:
        probe.connect((host, port))
        return True
    except OSError:
        return False
    finally:
        probe.close()


def create_server_socket(host, port):
    """Bind and listen, refusing to start when the port is already served."""
    if port_in_use(host, port):
        raise SystemExit(
            "Cannot start: %s:%d is already in use.\n"
            "\n"
            "A server is probably already running in another terminal. If so it is\n"
            "already serving clients, so you can simply use it - or stop it with:\n"
            "\n"
            "    netstat -ano | findstr %d      (find the PID listening on the port)\n"
            "    taskkill /PID <pid> /F         (stop that process)\n"
            "\n"
            "Or run this server on a free port instead:\n"
            "\n"
            "    python server.py --port %d\n"
            "    python client.py --port %d\n"
            % (host, port, port, port + 1, port + 1)
        )
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    return server_socket


def handle_connection(connection):
    """Receive one JSON message and reply with the analysis (or an error)."""
    connection.settimeout(10.0)
    data = b""
    try:
        while not data.endswith(b"\n"):
            chunk = connection.recv(4096)
            if not chunk:
                break
            data += chunk
            if len(data) > MAX_MESSAGE:
                break
    except socket.timeout:
        pass

    try:
        payload = json.loads(data.decode("utf-8").strip() or "[]")
        if not isinstance(payload, list):
            raise ValueError("payload must be a JSON list of records")
        response = {"ok": True, "analysis": analyze_records(payload)}
    except Exception as exc:  # noqa: BLE001 - report any bad input to the client
        response = {"ok": False, "error": "%s: %s" % (type(exc).__name__, exc)}

    connection.sendall((json.dumps(response) + "\n").encode("utf-8"))


def serve(host="127.0.0.1", port=65432, once=False, server_socket=None, verbose=True):
    """Accept connections until stopped.  once=True serves a single client."""
    server_socket = server_socket or create_server_socket(host, port)
    if verbose:
        print("Server listening on %s:%d ..." % (host, server_socket.getsockname()[1]), flush=True)
    try:
        while True:
            try:
                connection, address = server_socket.accept()
            except OSError:
                break
            if verbose:
                print("Connection from %s:%d" % (address[0], address[1]), flush=True)
            try:
                handle_connection(connection)
            finally:
                connection.close()
            if once:
                break
    except KeyboardInterrupt:
        if verbose:
            print("\nServer stopped by user.")
    finally:
        try:
            server_socket.close()
        except OSError:
            pass


def main():
    parser = argparse.ArgumentParser(description="Electricity Consumption Analyzer - TCP server")
    parser.add_argument("--host", default="127.0.0.1", help="bind address (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=65432, help="TCP port (default: 65432)")
    parser.add_argument("--once", action="store_true", help="serve one client, then exit")
    arguments = parser.parse_args()
    serve(arguments.host, arguments.port, once=arguments.once)


if __name__ == "__main__":
    main()
