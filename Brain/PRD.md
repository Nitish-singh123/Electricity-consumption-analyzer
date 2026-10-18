# PRD — Electricity Consumption Analyzer (Web)

Status: Draft · Last updated: 2026-10-18  
Phase: documentation only (no application code changed)

This is the **product requirements** source of truth for turning the existing
TCP client/server analyzer into a secure, production-quality web application.

---

## 1. Vision

Give users a multi-user web app where they can **sign in** (email/password,
Google, or GitHub), **upload or select** a consumption CSV, **run the existing
analysis**, and **view and revisit saved reports**.

The current Python analyzer already contains the domain logic. The product wraps
that logic with identity, storage, and history **without changing analysis
results**.

## 2. Problem

Consumers rarely see how daily peak/off-peak usage adds up, whether consumption
is rising, or how much they can afford within a monthly budget. The existing
tool does this analysis well, but only as a local loopback TCP client/server:
no accounts, no persistence, no way to reopen a past run.

## 3. Current product (as-is)

Verified by reading `README.md`, `server.py`, `client.py`, `tests.py`,
`testcases.py`, the three CSVs, `report/page1.md`–`page4.md`, and committed
`outputs/`.

- **Shape:** TCP client reads CSV → JSON-over-TCP → server runs FSM + functional
  pipeline + SymPy → client prints a ranked report.
- **Audience today:** a course assignment (21CSC203P) with a 26.10.2026
  handwritten-report submission. That terminal usage and hard-copy workflow is
  **legacy context**, not a web-product requirement.
- **Not in scope of the as-is app:** authentication, HTTPS, database, saved
  reports, multi-user isolation.

## 4. Target users

| Persona | Need |
|---|---|
| Household consumer | Upload meter readings, understand usage level, see budget advice |
| Analyst / consultant | Keep several datasets and reports over time |
| Reviewer of the existing assignment | Confirm FSM / TOU / slab / trend / budget numbers still match |

## 5. Goals (Phase 1 web product)

- G1 Sign in with **email/password**, **Google**, or **GitHub**.
- G2 **Upload a CSV** with the existing schema, or **select a bundled sample**.
- G3 **Run analysis** with the preserved engine and view a structured report.
- G4 **Save** every run and **revisit** it later without silent recomputation.
- G5 Secure by default: per-user isolation, validated uploads, no secret leakage.

## 6. Non-goals (Phase 1)

- Real-time smart-meter streaming.
- Payment processing or utility-company integrations.
- Forecasting beyond the existing least-squares trend.
- Native mobile apps, offline-first, multi-tenant org management.
- Visual/brand design (deferred — `DESIGN.md` is undecided).
- Replacing the assignment’s TCP demo until an explicit decision (D-5).

---

## 7. Preserved behavior — HARD INVARIANTS

Taken from `server.py` and locked by `tests.py` / the three live datasets.
Any change requires an ADR in `DECISIONS.md`.

| ID | Invariant | Exact current behavior |
|---|---|---|
| INV-1 | Daily FSM bands | `total_units < 10` → `LT10`; `< 20` → `B10_19`; `< 30` → `B20_29`; else `GE30` (i.e. under 10, 10–19, 20–29, 30+) |
| INV-2 | FSM states | `LOW`, `MODERATE`, `HIGH`, `OVERLOAD`. Start state is always `LOW`. |
| INV-3 | Transitions | 4×4 = 16 entries. Next state is the band’s target (`BAND_TARGET`). Relapse is allowed (e.g. `OVERLOAD` + 5 units → `LOW`). |
| INV-4 | High-usage records | `total_units >= 20` (inclusive) |
| INV-5 | TOU bill | `peak_units × 4 + offpeak_units × 2`, rounded to 2 dp. Default rates from `make_bill_calculator(4.0, 2.0)`. |
| INV-6 | Slab bill | first 50 units @ Rs 3/unit, then Rs 5/unit: `3x` if `x ≤ 50`, else `150 + 5(x − 50)` |
| INV-7 | Monthly budget | Rs 500. Break-even solves the **slab** piecewise for `bill(x) = 500`, keeping the in-domain root → **120 units**. Over-budget flag uses **slab bill**, not TOU: `bill_amount(total_units) > 500`. |
| INV-8 | Trend | least-squares `y = a·x + b` by solving normal equations in SymPy; `day_totals[0]` is day 1; predict day `n+1` rounded to 2 dp. Fewer than 2 days: `a = 0`, `b = units[0]`. Equation string uses 4 dp and never prints `+ -`. |
| INV-9 | CSV columns | `record_id`, `customer_id`, `customer_name`, `date`, `day_index`, `peak_units`, `offpeak_units` |
| INV-10 | Validity | Invalid if `peak_units` or `offpeak_units` is missing or `< 0`. Invalid rows are counted, listed, and excluded from analysis. |
| INV-11 | Distinct billing | TOU and slab are computed and reported **separately**. Grand total bill is TOU. Per-customer report shows both. Do not substitute one for the other. |

### Golden results (must be reproduced)

Recorded live on 2026-10-18 (`python testcases.py all` and `python -m unittest -v`).

| Case | Dataset | Expected |
|---|---|---|
| TC1 | `dataset.csv` | 12 received / 12 analyzed / 0 invalid; 4 customers; 223 units; TOU **Rs 780**; avg 18.58; rank 1 = **C03 Arun Prasad** (100 units, TOU 354, slab 400, OVERLOAD); C01 path `LOW → MODERATE → MODERATE → HIGH`, trend `y = 7.0000x + 4.6667`, day-4 **32.67**; 4 high-usage records; budget max **120**; over budget **none** |
| TC2 | `dataset_high.csv` | 9 / 9 / 0; 3 customers; 291 units; TOU **Rs 1040**; C07 slab **Rs 600 > 500** → over budget **C07**; C07 trend `y = 2.0000x + 42.6667` → **50.67**; C09 path `LOW → LOW → MODERATE → HIGH`; 7 high-usage records |
| TC3 | `dataset_edge.csv` | 10 / 9 / 1 invalid (C11 negative peak); 191 units; TOU **Rs 660**; C10 daily 10/20/30 → `LOW → MODERATE → HIGH → OVERLOAD`; C05 relapse `LOW → OVERLOAD → MODERATE → OVERLOAD`; C06 zero day; C10 trend `y = 10.0000x + 0.0000` → **40**; none over budget |

Empty over-budget lists are stored as `["none"]` in the analysis JSON (printer joins that list). Preserve that contract unless an ADR changes it.

README / `report/page4.md` sometimes write FSM paths without the start `LOW`
(e.g. C10 “MODERATE → HIGH → OVERLOAD”). The engine always prepends `LOW`.
**Goldens are the live `fsm_path` arrays**, not the shorthand. Trend strings in
README may omit `.0000` padding (`y = 7x + 4.6667` vs `y = 7.0000x + 4.6667`);
numeric values match. Committed `outputs/*.txt` titles omit the dataset filename
that live `testcases.py` now prints; numbers match.

---

## 8. Functional requirements

### FR-A Authentication
- FR-A1 Email + password sign-up / sign-in, email verification, password reset.
- FR-A2 Google OAuth.
- FR-A3 GitHub OAuth.
- FR-A4 Authenticated session with logout (including logout-everywhere). Session
  transport (httpOnly cookie BFF vs bearer) is **D-4**, not frozen here.
- FR-A5 Account-linking when the same email arrives via password and OAuth is
  **D-2**.

### FR-B Datasets
- FR-B1 Upload a CSV matching INV-9; reject missing headers / unreadable files
  with actionable errors.
- FR-B2 Select bundled samples: `dataset.csv`, `dataset_high.csv`, `dataset_edge.csv`.
- FR-B3 Preview + validation summary (received / analyzed / invalid) before or
  with the run. Row-level invalid data must not crash the run (INV-10).
- FR-B4 Datasets are private to the owner; list, rename, delete.

### FR-C Analysis and reports
- FR-C1 Run the preserved engine; return the same structured result `analyze_records`
  produces today (see `ARCHITECTURE.md` §1.4).
- FR-C2 Every run is stored as a **Report** (inputs + result snapshot + timestamp +
  engine version).
- FR-C3 Report view shows: received/analyzed/invalid counts; totals; per-customer
  ranking with FSM path, final state, recommendation, TOU bill, slab bill, trend
  equation, next-day prediction; high-usage records; budget advice.
- FR-C4 Re-open a past report from the snapshot (no silent recompute). Optional
  explicit “re-run” creates a **new** report.

### FR-D Export / sharing (minimal)
- FR-D1 Safe download of a report (format is D-6).
- FR-D2 Read-only share links are optional and unresolved (D-6).

## 9. Non-functional requirements

- NFR-1 Security: per-user isolation in API **and** database (RLS); OWASP ASVS L1 floor.
- NFR-2 Correctness: goldens in §7 stay green in CI.
- NFR-3 Performance: ≤10k rows analyzed in < 2 s p95 server time (proposed; unmeasured).
- NFR-4 Phase 1 may be single-region.
- NFR-5 Accessibility: WCAG 2.1 AA targets.
- NFR-6 Observability: structured logs, request IDs; no PII / raw CSV / tokens in logs.
- NFR-7 Local run documented (one command per service).

## 10. Assumptions

- A1 Existing Python analysis is authoritative; web wrapping must not drift.
- A2 Uploads are small-to-moderate CSVs, not streaming meters.
- A3 Customer names in CSVs are treated as personal data.
- A4 Phase 1 is single-tenant (one app, many users, no orgs).
- A5 Next.js + FastAPI + Supabase is the **proposed default** stack, not yet accepted
  (ADR-010–012).
- A6 Currency is Indian rupees as in the current report copy (`Rs`). Figma mocks
  use **USD and made-up kWh/bill figures**; those are illustration only and do
  **not** override this assumption or INV-5…INV-7.

## 11. Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Behavior drift vs terminal app | High | Extract engine unchanged; golden tests in CI |
| CSV abuse (size, formula injection) | High | Caps + safe export encoding |
| OAuth account-linking mistakes | Medium | Explicit D-2 before implementing |
| Visual design chosen too early | Medium | `DESIGN.md` stays undecided |
| RLS / secret leakage | High | Isolation tests; never commit service keys |
| Two-runtime ops (Node + Python) | Medium | Documented local/dev/prod; health checks |

## 12. Success metrics

- M1 New user: sign-in → upload or sample → analyse → saved report in < 3 minutes.
- M2 100% of goldens pass in CI.
- M3 Zero cross-user data exposure in authorization tests.
- M4 Valid CSVs analyse without 5xx.

## 13. Release criteria (Phase 1)

- FR-A / FR-B / FR-C implemented; FR-D minimal.
- Goldens + authz tests green in CI.
- Environments and rollback documented.

## 14. Open questions

See `DECISIONS.md` D-1…D-8. Highest product impact: account linking, session
strategy, fate of the TCP CLI, export/share policy, and visual direction (D-8:
Figma “Current” is now observed in `DESIGN.md` §8, still unaccepted). Also
decide household-mock vs multi-customer report, and CSV 5-column guide vs INV-9.
