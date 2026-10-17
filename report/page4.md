# PAGE 4 — Test Cases + Output Analysis + Conclusion
*(Handwrite this on A4 sheet 4 — attach the printed outputs separately)*

---

## 1. Test Cases (3 main scenarios + appendix of 17 automated tests)

### TEST CASE 1 — Normal dataset through the full client/server system
*(Printed output: `outputs/testcase1_normal.txt`)*

**Procedure:** start `python server.py`, then `python client.py`
(dataset.csv — 4 consumers × 3 days = 12 records), or simply run
`python testcases.py 1`.

| # | Check | Expected | Actual | Result |
|---|---|---|---|---|
| 1 | Records analyzed | 12 valid, 0 invalid | 12 valid, 0 invalid | PASS |
| 2 | Grand total units (reduce) | 223.0 | 223 | PASS |
| 3 | Total TOU bill (closure) | Rs 780 | Rs 780 | PASS |
| 4 | Rank 1 consumer | C03 Arun (100 units) | C03 Arun — 100 units | PASS |
| 5 | Arun FSM final state | OVERLOAD (32, 33, 35 ≥ 30) | LOW→OVERLOAD×3, OVERLOAD | PASS |
| 6 | Ramesh FSM path (12, 18, 26) | LOW→MODERATE→MODERATE→HIGH | same | PASS |
| 7 | Ramesh trend (SymPy) | y = 7x + 4.6667; day-4 = 32.67 | y = 7.0000x + 4.6667; 32.67 | PASS |
| 8 | Budget max units (SymPy) | 500 → 120 units | 120 units | PASS |
| 9 | High-usage records (filter ≥ 20) | 4 (Arun ×3 + Ramesh day-3) | 4 | PASS |

### TEST CASE 2 — High-usage dataset (budget violation)
*(Printed output: `outputs/testcase2_high.txt` — run with `python testcases.py 2`)*

| # | Check | Expected | Actual | Result |
|---|---|---|---|---|
| 1 | Records / consumers | 9 / 3 | 9 / 3 | PASS |
| 2 | Grand total units | 291.0 | 291 | PASS |
| 3 | Total TOU bill | Rs 1040 | Rs 1040 | PASS |
| 4 | C07 Suresh slab bill vs Rs 500 budget | 600 > 500 → over budget | Rs 600; "Customers over budget: C07" | PASS |
| 5 | C07 trend & prediction (44, 48, 48) | y = 2x + 42.6667 → 50.67 | y = 2.0000x + 42.6667 → 50.67 | PASS |
| 6 | C09 Iqbal FSM path (9, 12, 28) | LOW→LOW→MODERATE→HIGH | same | PASS |
| 7 | High-usage records (filter ≥ 20) | 7 | 7 | PASS |

### TEST CASE 3 — Edge-case dataset (FSM boundaries, relapse, invalid input)
*(Printed output: `outputs/testcase3_edge.txt` — run with `python testcases.py 3`)*

| # | Check | Expected | Actual | Result |
|---|---|---|---|---|
| 1 | Records received / analyzed / invalid | 10 / 9 / 1 | 10 / 9 / 1 | PASS |
| 2 | Invalid record handling (−5.0 units) | rejected, not crashed | reported as invalid: 1 | PASS |
| 3 | Consumers analyzed | 3 (C11 dropped: its only row invalid) | 3 | PASS |
| 4 | Grand total units | 191.0 | 191 | PASS |
| 5 | **Exact FSM boundaries** — C10 reads 10, 20, 30 | MODERATE → HIGH → OVERLOAD | LOW→MODERATE→HIGH→OVERLOAD | PASS |
| 6 | C05 relapse path (37, 12, 40) | OVERLOAD → MODERATE → OVERLOAD | LOW→OVERLOAD→MODERATE→OVERLOAD | PASS |
| 7 | C06 zero usage (0, 17, 25) | LOW day-1, ends HIGH | LOW→LOW→MODERATE→HIGH | PASS |
| 8 | C10 trend (10, 20, 30) | y = 10x + 0 → day-4 = 40 units | y = 10.0000x + 0.0000 → 40 | PASS |
| 9 | Trend sign formatting (C06, falling to negative intercept) | "y = 12.5x − 11", never "+ −" | y = 12.5000x - 11.0000 | PASS |
| 10 | Budget solve | Rs 500 → 120 units, none over budget | 120 units, none | PASS |

### APPENDIX — Automated test suite (supporting evidence)
*(Printed output: `outputs/appendix_unit_tests.txt` — run: `python -m unittest -v`)*

| Test class | Tests | What it proves | Result |
|---|---|---|---|
| FSMTests | 4 | Band boundaries (9.9/10, 19.9/20, 29.9/30), all 16 transitions, FSM path | ok |
| FunctionalProgrammingTests | 4 | Closure rates, custom-rate closure, map enrich, filter + reduce totals | ok |
| SymPyTests | 4 | Slab bills (36/150/200), trend 7x+4.6667, budget solve (150→50, 200→60), sign formatting | ok |
| IntegrationTests | 3 | Real TCP end-to-end, malformed JSON rejected, double-bind refused safely | ok |
| EdgeCaseTests | 2 | Negative/missing fields reported not crashed; single-day consumer | ok |

**Final result: `Ran 17 tests … OK` — all tests pass.**

---

## 2. Output Analysis

* The client/server system transferred every record correctly over TCP
  (JSON + newline protocol) and returned a structured analysis in the same
  format for all three scenarios — the report layout is identical each run.
* **Functional programming** concepts produced verified aggregates:
  223 units / Rs 780 (TC1), 291 units / Rs 1040 (TC2) and 191 units / Rs 660
  (TC3) — each confirmed by independent manual sums in the automated tests.
* The **FSM** behaved correctly in every scenario: continuous overload
  (Arun), escalation (Ramesh, Iqbal, Vikram), steady low usage (Divya),
  exact boundary classification at 10/20/30 units (C10, TC3), and a
  relapse after recovery (Anita, TC3) — matching the recorded readings.
* **SymPy** results were numerically exact: the fitted least-squares trend
  lines predicted the next day's consumption sensibly, and the budget
  break-even solve correctly flagged C07 (Rs 600 > Rs 500) in TC2 while
  clearing all consumers in TC1 and TC3.
* Error handling was robust: an invalid reading (−5.0 units) was reported as
  `invalid: 1` without disturbing the analysis, and malformed JSON received an
  `{"ok": false, "error": …}` reply instead of crashing the server. During
  development a second server instance was also refused safely (double-bind
  guard), so the demo can never silently answer from stale code.

---

## 3. Conclusion

The **Electricity Consumption Analyzer** successfully integrates all four
mandatory pillars of the assignment into one working application:

1. **Functional programming** (map, filter, reduce, lambda, higher-order
   function/closure) gives a clean, declarative analysis pipeline.
2. **TCP client/server socket programming** transports records and results
   between two independent Python programs using a simple JSON protocol.
3. A **4-state FSM** classifies each consumer's daily usage and produces a
   final status with an actionable recommendation.
4. **SymPy** performs genuine symbolic mathematics: a piecewise tariff model,
   least-squares trend fitting by solving the normal equations, and a budget
   break-even solution.

The application passes all 17 automated tests and all three live end-to-end
scenarios, and it fails safely on invalid data or duplicate server instances.
It is easily extensible — more consumers, days or tariff slabs can be added to
the CSV without changing the logic.

**Submission deadline: 26.10.2026**
