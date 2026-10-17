# Electricity Consumption Analyzer

**21CSC203P — Advanced Programming Practice · Individual Integrated Assignment**
Topic (Rolls 66–69): **Electricity Consumption Analyzer** · Submission deadline: **26.10.2026**

A TCP client/server application that analyses daily electricity-consumption records of
several consumers using **Functional Programming**, a **4-state Finite State Machine**
and **SymPy** symbolic computing, then prints a ranked final analysis report.

---

## 1. Requirements

| Item | Version / note |
|---|---|
| Python | 3.9 or newer (developed and tested on 3.12.10) |
| SymPy | `pip install sympy` (already installed on the development machine) |
| Network | Local loopback only (`127.0.0.1`), no internet needed |

Install the one dependency:

```powershell
pip install sympy
```

---

## 2. Project files

| File | Purpose |
|---|---|
| `server.py` | TCP server. Holds the FSM, the functional pipeline and all SymPy logic |
| `client.py` | TCP client. Reads a CSV dataset, sends the records, prints the report |
| `testcases.py` | Test-case runner. Starts a server, runs one test case, prints only that output |
| `tests.py` | 17 automated tests (FSM, functional, SymPy, TCP integration, edge cases) |
| `dataset.csv` | Test case 1 dataset — 4 consumers × 3 days (12 records) |
| `dataset_high.csv` | Test case 2 dataset — 3 heavy-usage consumers (9 records) |
| `dataset_edge.csv` | Test case 3 dataset — FSM boundaries, relapse, zero usage, 1 invalid row (10 records) |
| `outputs/` | Generated printouts: the 3 test cases + unit-test appendix |
| `report/page1.md … page4.md` | Content for the 4 handwritten A4 pages of the hard-copy report |
| `start_server.bat`, `start_client.bat` | Double-click launchers (always run in the right folder) |
| `run_testcase.bat`, `run_tests.bat` | Double-click launchers for a test case / the test suite |

> **Important:** every command must run with the project folder as the current
> directory, otherwise Python cannot find `server.py`. Either `cd` first, or use
> the `.bat` launchers above which do it for you.
>
> ```powershell
> cd E:\opencode_projects\app_assignment
> ```

---

## 3. Quick start — no typing (double-click launchers)

These `.bat` files always switch to the project folder first, so they can be
double-clicked from anywhere:

| File | What it does |
|---|---|
| `start_server.bat` | Starts the server (keeps the window open) |
| `start_client.bat` | Runs the client for test case 1 (or drag a number: `start_client.bat 3`) |
| `run_testcase.bat` | Runs one test case end to end — `run_testcase.bat 1`, `2`, `3` or `all` |
| `run_tests.bat` | Runs the full 17-test suite |

---

## 4. How to run — one command per test case (recommended)

Try the `cd` command first, then each line starts a server on a free port, runs
the test case end to end and prints **only that test case's report**:

```powershell
cd E:\opencode_projects\app_assignment

python testcases.py 1      # Test case 1 - normal dataset
python testcases.py 2      # Test case 2 - high-usage dataset
python testcases.py 3      # Test case 3 - edge-case dataset
python testcases.py all    # All three test cases in order
```

---

## 5. How to run — live client/server demo (for the viva)

`cd` into the project folder, then open **two terminals**.

```powershell
# Terminal 1 — start the server (keeps running; press Ctrl+C to stop)
python server.py
```

```powershell
# Terminal 2 — run the client against it
python client.py                 # test case 1 (dataset.csv)
python client.py --testcase 2    # test case 2 (dataset_high.csv)
python client.py --testcase 3    # test case 3 (dataset_edge.csv)
python client.py --dataset dataset_edge.csv   # any custom dataset
python client.py --testcase 1 --verbose       # also show connection details
```

Server options:

```powershell
python server.py --port 7000     # use another port (client: --port 7000)
python server.py --once          # serve one client, then exit
```

> Starting a second server while one is already running is safe: it refuses to
> start and tells you how to stop the first one or use another port (this
> prevents clients from silently talking to an old server).

---

## 6. How to run the automated tests

```powershell
python -m unittest -v        # verbose, 17 tests
python -m unittest           # summary only
```

Expected result: **`Ran 17 tests … OK`**

---

## 7. Regenerating the printable outputs

```powershell
python testcases.py 1 > outputs\testcase1_normal.txt
python testcases.py 2 > outputs\testcase2_high.txt
python testcases.py 3 > outputs\testcase3_edge.txt
python -m unittest -v > outputs\appendix_unit_tests.txt
```

Then print the files listed in section 10.

---

## 8. Test cases and expected results

| TC | Dataset | Command | Key results |
|---|---|---|---|
| 1 | `dataset.csv` | `python testcases.py 1` | 12 records, 4 consumers, 223 units, Rs 780; C03 Arun = rank 1 (100 units, OVERLOAD); C01 Ramesh path LOW→MODERATE→MODERATE→HIGH, trend `y = 7x + 4.6667`, day-4 prediction 32.67 units; 4 high-usage records; budget Rs 500 → 120 units |
| 2 | `dataset_high.csv` | `python testcases.py 2` | 9 records, 3 consumers, 291 units, Rs 1040; C07 Suresh flagged over budget (slab bill Rs 600 > Rs 500); C07 trend `y = 2x + 42.6667` → 50.67 units; C09 Iqbal path LOW→LOW→MODERATE→HIGH; 7 high-usage records |
| 3 | `dataset_edge.csv` | `python testcases.py 3` | 10 records received, 9 analyzed, 1 invalid (negative reading); 191 units, Rs 660; exact FSM boundaries C10 = 10 → 20 → 30 units ⇒ MODERATE → HIGH → OVERLOAD; C05 relapse OVERLOAD→MODERATE→OVERLOAD; C06 zero-usage day; C10 trend `y = 10x` → 40 units |
| Appendix | — | `python -m unittest -v` | `Ran 17 tests … OK` |

---

## 9. Mandatory components — where to find them

| Requirement | Location |
|---|---|
| **Functional programming (5 concepts)** | `server.py` — `map` (`enrich`), `filter` (valid / high-usage), `reduce` (grand totals), `lambda` (keys, accumulators), higher-order function + closure (`make_bill_calculator`) |
| **TCP client/server (socket)** | `client.py` (`socket.create_connection`, `sendall`, `recv`) and `server.py` (`bind`, `listen`, `accept`, `recv`, `sendall`), JSON + newline protocol on port 65432 |
| **FSM (4 states)** | `server.py` — states `LOW / MODERATE / HIGH / OVERLOAD`, input bands `LT10 / B10_19 / B20_29 / GE30`, complete 16-entry `TRANSITIONS` table, `walk_fsm()` |
| **SymPy (3 symbolic operations)** | `server.py` — piecewise slab tariff (`bill_expr`, `bill_amount`), least-squares trend fit by solving the normal equations (`fit_trend`, `predict_day`), budget break-even solve (`budget_units`) |
| **≥3 test cases** | `testcases.py` (live scenarios 1–3) and `tests.py` (17 automated tests) |

**Wire protocol**

```
Client → Server :  [ {record}, {record}, ... ] \n       JSON list + newline
Server → Client :  { "ok": true, "analysis": {...} } \n  analysis (or an error)
```

---

## 10. What to print for the hard-copy submission

| # | File | Note |
|---|---|---|
| 1 | `server.py` | complete source code |
| 2 | `client.py` | complete source code |
| 3 | `testcases.py` | complete source code |
| 4 | `tests.py` | complete source code (shows all 17 tests) |
| 5 | `outputs\testcase1_normal.txt` | test case 1 output |
| 6 | `outputs\testcase2_high.txt` | test case 2 output |
| 7 | `outputs\testcase3_edge.txt` | test case 3 output |
| 8 | `outputs\appendix_unit_tests.txt` | appendix: 17/17 automated tests pass |
| 9 | `dataset.csv`, `dataset_high.csv`, `dataset_edge.csv` | recommended — shows your own datasets |

Print command (opens the Windows print dialog per file):

```powershell
notepad /p server.py
notepad /p client.py
notepad /p testcases.py
notepad /p tests.py
notepad /p outputs\testcase1_normal.txt
notepad /p outputs\testcase2_high.txt
notepad /p outputs\testcase3_edge.txt
notepad /p outputs\appendix_unit_tests.txt
notepad /p dataset.csv
notepad /p dataset_high.csv
notepad /p dataset_edge.csv
```

**Hard-copy assembly order**

1. Front page — Name, Register No., Section, Assigned Topic
2. 4 handwritten A4 pages (use `report\page1.md` … `report\page4.md` as the guide — write by hand)
3. Printed source code (`server.py`, `client.py`, `testcases.py`, `tests.py`)
4. Printed outputs (the 3 test cases + appendix)
5. Staple / file everything together

Do **not** print `report\page*.md` (they must be handwritten) and there are no other
generated files to submit.

---

## 11. Troubleshooting

| Symptom | Cause and fix |
|---|---|
| `can't open file '...\server.py': [Errno 2] No such file or directory` | The terminal is not in the project folder. Run `cd E:\opencode_projects\app_assignment` first, or use `start_server.bat` |
| `'python' is not recognized as an internal or external command` / `The term 'python' is not recognized` | Python is not on your PATH. Use `py -3 server.py` instead, or reinstall Python with "Add python.exe to PATH" |
| `Python was not found; run without arguments to install from the Microsoft Store` | Windows opened the Store alias, not real Python. Run `py -3 server.py` (or disable the alias in Settings → Apps → App execution aliases) |
| `SymPy is not installed for this Python interpreter` | Run `pip install sympy`. Check the interpreter with `python -c "import sys; print(sys.executable)"` |
| `Cannot start: 127.0.0.1:65432 is already in use` | A server is already running. Use it, or stop it: `netstat -ano \| findstr 65432` then `taskkill /PID <pid> /F`, or use `python server.py --port 65433` and `python client.py --port 65433` |
| `could not reach the server at 127.0.0.1:65432` | The server is not running. Start it in another terminal (`python server.py`), or use `python testcases.py <n>` which starts its own server |
| `Cannot read the dataset '...'` | Wrong `--dataset` value or wrong folder. Use `--testcase 1\|2\|3`, or run from the project folder |
| Client prints nothing / seems to hang | The server terminal must be open and show `Server listening on 127.0.0.1:65432 ...` |
| Check which process owns the port | `netstat -ano \| findstr 65432` |
| Use a different Python | Replace `python` with `py -3` in every command |
| Window closes immediately when double-clicking | Use the provided `.bat` launchers — they keep the window open |
