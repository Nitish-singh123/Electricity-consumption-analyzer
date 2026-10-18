# TEST_PLAN

Status: Draft · Last updated: 2026-10-18  
Covers the **current baseline** (commands actually run this phase) and the
planned web-app test strategy. Results below are only those executed here.

---

## 1. Recorded baseline (executed 2026-10-18)

Environment: Windows 10, Python **3.12.10**
(`C:\Users\itsak\AppData\Local\Programs\Python\Python312\python.exe`),
SymPy **1.14.0**. Working directory: `E:\opencode_projects\app_assignment`.

### 1.1 Unit/integration suite

Command: `python -m unittest -v`

Result (verbatim ending, Phase 0 re-run 2026-10-18 afternoon):

```
Ran 17 tests in 0.316s

OK
```

An earlier same-day run also ended `Ran 17 tests in 0.496s` / `OK`. Duration varies; the
pass/fail result is what matters.

All 17 tests reported `ok`:

| Class | Tests |
|---|---|
| `FSMTests` | `test_input_band_boundaries`, `test_transition_boundaries`, `test_transition_table_is_complete`, `test_fsm_path_for_rising_usage` |
| `FunctionalProgrammingTests` | `test_default_tou_closure`, `test_closure_with_custom_rates`, `test_map_enrich_does_not_mutate_input`, `test_filter_and_reduce_pipeline` |
| `SymPyTests` | `test_slab_bill`, `test_trend_fit_and_prediction`, `test_budget_break_even_solve`, `test_trend_equation_sign_formatting` |
| `IntegrationTests` | `test_end_to_end_analysis`, `test_server_refuses_double_bind`, `test_malformed_json_is_rejected_gracefully` |
| `EdgeCaseTests` | `test_invalid_records_are_reported_not_crashing`, `test_single_day_consumer` |

### 1.2 Live test cases

Command: `python testcases.py all` — **exit 0**.

Headline numbers matched README / committed `outputs/` (and `PRD.md` goldens):

| Case | Received | Analyzed | Invalid | Customers | Units | TOU bill | Avg/record | Over budget |
|---|---|---|---|---|---|---|---|---|
| TC1 `dataset.csv` | 12 | 12 | 0 | 4 | 223 | Rs 780 | 18.58 | none |
| TC2 `dataset_high.csv` | 9 | 9 | 0 | 3 | 291 | Rs 1040 | 32.33 | C07 |
| TC3 `dataset_edge.csv` | 10 | 9 | 1 | 3 | 191 | Rs 660 | 21.22 | none |

Additional live values (must stay stable):

- TC1 rank 1: C03, 100 units, OVERLOAD, trend `y = 1.5000x + 30.3333`, day-4 36.33.
- TC1 C01: path `LOW → MODERATE → MODERATE → HIGH`, `y = 7.0000x + 4.6667`, day-4 32.67.
- TC1 budget max units: 120; 4 high-usage records.
- TC2 C07: 140 units, TOU Rs 506, **slab Rs 600**, `y = 2.0000x + 42.6667` → 50.67.
- TC2 C09: `LOW → LOW → MODERATE → HIGH`; 7 high-usage records.
- TC3 C10: daily 10 → 20 → 30; path `LOW → MODERATE → HIGH → OVERLOAD`; `y = 10.0000x + 0.0000` → 40.
- TC3 C05 relapse: `LOW → OVERLOAD → MODERATE → OVERLOAD`.
- TC3 C06: daily 0 → 17 → 25; `y = 12.5000x - 11.0000`.

**Title drift vs committed `outputs/`:** live `testcases.py` titles include the
filename, e.g. `TEST CASE 1 - NORMAL DATASET (dataset.csv)`. Committed
`outputs/testcase1_normal.txt` uses `TEST CASE 1 - NORMAL DATASET` without the
parenthetical. Numeric content matches. Do not treat the title strings as a
golden unless Stage 1 regenerates `outputs/`.

### 1.3 Not run this phase

- `pytest` (not configured).
- Browser / Playwright.
- Load tests.
- Any modified application tests (none exist yet for a web stack).

Committed `outputs/appendix_unit_tests.txt` also shows `Ran 17 tests … OK` from
an earlier run (`0.330s`). That file was **not** regenerated this phase.

---

## 2. Characterization tests to keep forever (G-series)

These lock `tests.py` behavior so a core extraction cannot drift:

- G-01 `band()`: 9.9→LT10, 10→B10_19, 19.9→B10_19, 20→B20_29, 29.9→B20_29, 30→GE30.
- G-02 `fsm_next("OVERLOAD", 5) == "LOW"`.
- G-03 `len(TRANSITIONS) == 16`.
- G-04 `walk_fsm("LOW", [12, 18, 26]) == [LOW, MODERATE, MODERATE, HIGH]`.
- G-05 `TOU_BILL(8, 4) == 40.0`; custom `(5, 3)` on (8, 4) → 52.0.
- G-06 `enrich` does not mutate input; 8+4 → total 12, TOU 40.
- G-07 `bill_amount(12)=36`, `(50)=150`, `(60)=200`.
- G-08 `fit_trend([12, 18, 26]) = (7.0, 14/3)`; `predict_day(..., 4) = 32.67`.
- G-09 `budget_units(150)=50`, `(200)=60`, `(100) ≈ 33.33`.
- G-10 Trend strings: `y = 7.0000x + 4.6667` and `y = 12.5000x - 11.0000`.
- G-11 Invalid mix: analyzed 1, invalid 2, units 4.0.
- G-12 Single-day 5+5: path `[LOW, MODERATE]`, prediction 10.0.
- G-13 Full TC1/TC2/TC3 result equality (numeric fields, not printer titles).

---

## 3. Planned web test levels

| Level | Scope | Proposed tooling |
|---|---|---|
| Unit | `analyzer_core` | pytest wrapping/moving current unittests |
| Golden | TC1–TC3 + G-series | pytest |
| Contract | FastAPI schemas / error envelope | pytest |
| Integration | API + Postgres + Storage | pytest + test DB |
| Authorization | Cross-user denial on every table | pytest + RLS |
| E2E | Three sign-in methods → upload → run → revisit | Playwright (after UI exists) |
| Security | Auth abuse, upload abuse, injection, headers | see `SECURITY.md` |
| Performance | NFR-3 once an HTTP path exists | k6/locust light |
| Accessibility | Core flows | axe + manual |

Do not mark any of these as passing until they are implemented and executed.

## 4. Planned web cases (not yet implemented)

### Auth
A-01 sign-up / verify / sign-in · A-02 wrong password · A-03 reset ·
A-04 Google · A-05 GitHub · A-06 session expiry / logout-everywhere ·
A-07 linking per D-2.

### Datasets
D-01 valid CSV · D-02 missing columns · D-03 bad types · D-04 size/row caps ·
D-05 encoding · D-06 negative readings invalid not fatal · D-07 isolation ·
D-08 duplicate upload policy.

### Reports
R-01 goldens via API · R-02 snapshot persisted · R-03 reopen without recompute ·
R-04 engine_version on re-run · R-05 safe export · R-06 user-scoped list.

## 5. CI gates (when a web pipeline exists)

1. Lint / format / types.
2. Unit + goldens (must match Stage 0 numbers).
3. Contract + RLS isolation.
4. Build API + web.
5. SCA / SAST.
6. E2E on staging or main.

## 6. Coverage targets (proposed, not measured)

- `analyzer_core`: ≥ 95% line/branch.
- Authorization: isolation test per user-owned table.
- No P0/P1 open at Phase 1 release.
