# PAGE 2 — System Architecture + Algorithm / Flowchart
*(Handwrite this on A4 sheet 2 — draw the diagrams by hand)*

---

## 1. System Architecture

```
┌──────────────────────────────────────────────────────── TCP (port 65432) ─┐

┌──────────────┐   read CSV     ┌────────────────────┐   JSON list of     ┌────────────────────────┐
│ dataset.csv  │ ─────────────► │     CLIENT         │   records (\n)     │        SERVER          │
│ 12 records   │                │   client.py        │ ─────────────────► │      server.py         │
└──────────────┘                │  - load_dataset()  │                    │  - accept() / recv()   │
                                │  - send_records()  │ ◄───────────────── │  - analyze_records()   │
                                │  - print_report()  │   JSON analysis    │      ├ FP pipeline      │
                                └────────────────────┘                    │      ├ FSM engine       │
      Terminal 2               socket.create_connection                   │      └ SymPy engine     │   Terminal 1
                                                                          └────────────────────────┘
```

**Components:**

1. **Dataset (`dataset.csv`)** — 12 original records: 4 consumers
   (C01 Ramesh, C02 Divya, C03 Arun, C04 Kavya) × 3 days, each record holding
   `peak_units` and `offpeak_units`. Two more datasets are used for the other
   test cases: `dataset_high.csv` (3 heavy-usage consumers, test case 2) and
   `dataset_edge.csv` (FSM boundary values 10/20/30, a relapse, a zero-usage
   day and one invalid row, test case 3).
2. **Client (`client.py`)** — reads the CSV, converts rows to typed Python
   dictionaries, serialises them as a JSON list terminated by `\n`, sends them
   to the server over a TCP socket, waits for the reply, and pretty-prints the
   analysis report.
3. **Server (`server.py`)** — listens on `127.0.0.1:65432`. For every
   connection it receives one JSON message, runs the full analysis pipeline
   (FP → FSM → SymPy) and replies with one JSON object.
4. **Test-case runner (`testcases.py`)** — one command per test case
   (`python testcases.py 1`) starts the server, runs the test case end to end
   and prints only that test case's report.
5. **Tests (`tests.py`)** — 17 tests; the integration tests start a real TCP
   server on an ephemeral port and drive the real client against it.

**Wire protocol (simple and robust):**

```
Client → Server :  [ {record}, {record}, ... ] \n      (JSON list + newline)
Server → Client :  { "ok": true, "analysis": {...} } \n (one JSON object)
                  or  { "ok": false, "error": "..." } \n on bad input
```

---

## 2. Algorithm

**Client side**
1. Read CSV file; convert each row to a record dictionary (floats for units).
2. Connect to server at `127.0.0.1:65432` (retry a few times if not ready).
3. Send the JSON list of records followed by `\n`.
4. Receive the reply until `\n`; parse JSON; print the final report.

**Server side (per connection)**
1. Receive bytes until `\n`; decode and `json.loads` the record list.
2. **Filter** out invalid records (missing or negative readings).
3. **Map** each valid record → enriched record
   (`total_units = peak + offpeak`, `tou_bill` from the tariff closure).
4. For each consumer (grouped by `customer_id`, ordered by `day_index`):
   a. Run daily totals through the **FSM** → state path and final state.
   b. **Reduce** daily values → consumer total units and total bill.
   c. Symbolically fit the trend line `y = a·x + b` (**SymPy** least squares)
      and predict the next day's consumption.
   d. Evaluate the symbolic slab tariff for the consumer's total units.
5. **Filter** high-usage records (≥ 20 units/day) for the warnings section.
6. Compute grand totals with **reduce**; rank consumers with
   `sorted(key=lambda ...)`.
7. Solve the budget break-even (**SymPy**) for Rs 500 monthly budget.
8. Send the complete analysis back to the client as JSON.

---

## 3. Flowchart (draw by hand)

```
        ┌─────────┐
        │  START   │
        └────┬────┘
             ▼
   ┌───────────────────┐      ┌──────────────────────┐
   │ Client reads CSV  │      │ Server: bind/listen  │
   │ dataset (12 rows) │      │ socket :65432        │
   └─────────┬─────────┘      └──────────┬───────────┘
             ▼                           ▼
   ┌───────────────────┐      ┌──────────────────────┐
   │ TCP connect +     │      │ accept() connection  │◄─────┐
   │ send JSON records │ ───► │ recv() until '\n'    │      │
   └─────────┬─────────┘      └──────────┬───────────┘      │
             │                           ▼                  │
             │                ┌──────────────────────┐      │
             │                │ Filter invalid recs  │      │
             │                │ Map → bill dicts     │      │
             │                └──────────┬───────────┘      │
             │                           ▼                  │
             │                ┌──────────────────────┐      │
             │                │ Per consumer:        │      │
             │                │  FSM path (4 states) │      │
             │                │  Reduce → totals     │      │
             │                │  SymPy trend + bill  │      │
             │                └──────────┬───────────┘      │
             │                           ▼                  │
             │                ┌──────────────────────┐      │
             │                │ SymPy budget solve   │      │
             │                │ build analysis JSON  │      │
             │                └──────────┬───────────┘      │
             ▼                           ▼                  │
   ┌───────────────────┐      ┌──────────────────────┐      │
   │ print final       │ ◄─── │ send reply + newline │ ─────┘
   │ analysis report   │      │ (loop for next       │   more clients?
   └─────────┬─────────┘      │  connection)         │
             ▼                └──────────────────────┘
        ┌─────────┐
        │   END   │
        └─────────┘
```
