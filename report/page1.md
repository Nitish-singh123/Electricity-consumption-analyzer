# PAGE 1 — Title, Problem Statement and Objectives
*(Handwrite this on A4 sheet 1)*

---

## Title
**ELECTRICITY CONSUMPTION ANALYZER — A TCP Client/Server Application with FSM and SymPy**

Course: 21CSC203P — Advanced Programming Practice
Assignment: Individual Integrated Assignment (Python Paradigm, Automata & Symbolic Computing Challenge)
Rolls 66–69 allotted topic: **Electricity Consumption Analyzer**

---

## 1. Problem Statement

Electricity consumers receive bills but rarely understand *how* their daily usage
behaviour adds up, whether their consumption is rising, or how much they can
afford to consume within a monthly budget. Manual analysis of daily meter
readings is slow and error-prone.

The problem addressed by this application is:

> **Given a small dataset of daily peak and off-peak energy readings of several
> consumers, analyse each consumer's usage automatically — compute the bill,
> classify the daily usage level using a Finite State Machine, detect rising
> trends and budget violations using symbolic mathematics, and deliver the
> complete analysis over a TCP network from a server to a client.**

The solution must integrate the four pillars of this course:
functional programming, TCP client/server network programming, automata (FSM)
design and symbolic computing with SymPy.

---

## 2. Objectives

1. **Create a small original dataset** of electricity consumption records
   (customer id, name, date, day index, peak units, off-peak units) — 12 records
   of 4 consumers over 3 days.
2. **Build a TCP client** (Python `socket`) that reads the CSV dataset and
   sends the records to the server as JSON messages.
3. **Build a TCP server** that receives the records and performs the complete
   analysis, then sends the result back to the client.
4. **Apply functional programming** — at least 3 concepts are used in the real
   code: `map`, `filter`, `reduce`, `lambda`, and a higher-order function that
   returns a bill-calculator **closure**.
5. **Design a Finite State Machine** with 4 states
   (LOW → MODERATE → HIGH → OVERLOAD) that tracks each consumer's daily usage
   level and produces a final status + recommendation.
6. **Use SymPy meaningfully** for three symbolic operations: the piecewise
   slab-tariff model, least-squares trend fitting by solving normal equations,
   and the budget break-even solve.
7. **Test the application** with at least 3 test cases (17 unit/integration
   tests are written; 3 main ones are documented on page 4) and generate a
   meaningful final analysis report.

---

## 3. Scope and Requirements Met

| Requirement | Where it is implemented |
|---|---|
| Functional programming (≥3 concepts) | `server.py` — map / filter / reduce / lambda / closure |
| TCP Client/Server (socket) | `client.py` (sender) + `server.py` (receiver), JSON over TCP port 65432 |
| FSM (≥3 states) | `server.py` section 1 — 4 states, 16-transition table |
| SymPy (meaningful operation) | `server.py` section 2 — tariff model, trend fit, budget solve |
| ≥3 test cases | `tests.py` — 17 tests in 5 classes; 3 documented on page 4 |
