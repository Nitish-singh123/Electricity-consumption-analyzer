"""
Test case runner - Electricity Consumption Analyzer.

Runs a prepared test case end to end: it starts the TCP server on a free local
port, sends the selected dataset through the real client, prints ONLY that test
case's analysis report and shuts the server down again.

    python testcases.py 1      # test case 1 - normal dataset
    python testcases.py 2      # test case 2 - high-usage dataset
    python testcases.py 3      # test case 3 - edge-case dataset
    python testcases.py all    # run all three test cases in order
"""

import sys
import threading

import client
import server


def run_testcase(case_number):
    """Run one test case end to end and print its report."""
    case_title, dataset = client.TESTCASES[case_number]
    try:
        records = client.load_dataset(dataset)
    except (FileNotFoundError, OSError):
        raise SystemExit(
            "Cannot read the dataset '%s'.\n"
            "The test cases expect the dataset files to be in %s"
            % (dataset, client.BASE_DIR)
        )

    server_socket = server.create_server_socket("127.0.0.1", 0)
    port = server_socket.getsockname()[1]
    worker = threading.Thread(
        target=server.serve,
        kwargs={"server_socket": server_socket, "once": True, "verbose": False},
        daemon=True,
    )
    worker.start()
    try:
        analysis = client.send_records("127.0.0.1", port, records)
    finally:
        server_socket.close()
        worker.join(timeout=5)

    client.print_report(
        analysis,
        title="TEST CASE %d - %s (%s)" % (case_number, case_title.upper(), dataset),
    )


def main():
    usage = "usage: python testcases.py <1|2|3|all>"
    if len(sys.argv) != 2:
        print(usage)
        raise SystemExit(2)

    choice = sys.argv[1].lower()
    if choice == "all":
        numbers = sorted(client.TESTCASES)
    elif choice.isdigit() and int(choice) in client.TESTCASES:
        numbers = [int(choice)]
    else:
        print(usage)
        raise SystemExit(2)

    for case_number in numbers:
        run_testcase(case_number)
        if case_number != numbers[-1]:
            print()


if __name__ == "__main__":
    main()
