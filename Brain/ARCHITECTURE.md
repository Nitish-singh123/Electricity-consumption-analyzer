# ARCHITECTURE — Electricity Consumption Analyzer (Web)

Status: Draft · Last updated: 2026-10-18  
This document describes the **as-is** architecture (verified by inspection) and a
**proposed default** target (Next.js/TypeScript UI, FastAPI/Python API, Supabase
Auth/PostgreSQL). The stack is a proposal, not an accepted decision. No
implementation has begun.

---

## 1. As-is (verified)

### 1.1 Components

```
dataset*.csv  →  client.py  ──TCP JSON\\n──▶  server.py
                 load_dataset                     analyze_records
                 print_report                     FSM + FP + SymPy

testcases.py  →  ephemeral TCP server (port 0) + client.send_records + print_report
tests.py      →  17 unittests (in-process engine + live TCP on port 0)
```

Repository root (git): `E:\opencode_projects\app_assignment`  
Parent folder `E:\opencode_projects` is **not** a git repository.

### 1.2 Module responsibilities

| Module | Responsibility | Key symbols |
|---|---|---|
| `server.py` | FSM, functional pipeline, SymPy, TCP server | `STATES`, `INPUT_BANDS`, `TRANSITIONS`, `band`, `fsm_next`, `walk_fsm`, `bill_expr`, `bill_amount`, `fit_trend`, `predict_day`, `budget_units`, `make_bill_calculator`, `TOU_BILL`, `is_valid`, `enrich`, `customer_summary`, `analyze_records`, `port_in_use`, `create_server_socket`, `handle_connection`, `serve` |
| `client.py` | CSV load, TCP send, report print | `TESTCASES`, `load_dataset`, `send_records`, `print_report` |
| `testcases.py` | One-shot live runner | `run_testcase` |
| `tests.py` | 5 classes, 17 tests | FSM, FP, SymPy, Integration, EdgeCase |

There is **no** separate analysis package. Domain logic lives inside `server.py`.

### 1.3 Wire protocol (current)

- Transport: TCP, default `127.0.0.1:65432` (`--host`, `--port`).
- Request: newline-terminated JSON **list** of records.
- Response: newline-terminated JSON object `{ "ok": true, "analysis": {…} }` or
  `{ "ok": false, "error": "Type: message" }`.
- Server: `MAX_MESSAGE = 10 MiB`; recv timeout 10 s; `listen(5)`; serial handling.
- Client: 8 connect retries at 0.4 s; 10 s timeout.
- Double-bind: `port_in_use` probe refuses a second server on the same port
  (Windows `SO_REUSEADDR` trap).

### 1.4 Analysis result contract (preserve)

```
{
  records_received, records_analyzed, records_invalid,
  invalid_records[], billed_records[], high_usage_records[],
  customers[ {
    rank, customer_id, customer_name, days, daily_units[],
    fsm_path[], final_state, recommendation,
    total_units, tou_bill, slab_bill,
    trend_a, trend_b, trend_equation, predicted_next_day_units
  } ],
  summary { customers, total_units, total_tou_bill, average_units_per_record },
  budget  { monthly_budget, max_units_allowed, customers_over_budget[] }
}
```

Notes:
- Ranking is by `total_units` descending.
- `summary.total_tou_bill` is the TOU grand total, not slab.
- `customers_over_budget` is a list of `customer_id`s, or `["none"]` if empty.
- `billed_records` include `total_units` and `tou_bill` (enrich does not add slab per day).

### 1.5 Runtime / repo facts

- Python **3.12.10**, SymPy **1.14.0** (this machine, 2026-10-18).
- No `pyproject.toml` / `setup.py` / `.gitignore`.
- `__pycache__/*.pyc` is **tracked** in git.
- Branch `master`, origin `https://github.com/Nitish-singh123/Electricity-consumption-analyzer.git`.
- Two commits: `d99b259` first changes · `e1ea890` second changes.

### 1.6 Gaps vs a production web product

No identity, no persistence, no HTTP API, no TLS, no rate limits, no multi-user
authorization, serial loopback server, analysis mixed with sockets.

---

## 2. Target — PROPOSED DEFAULT (not decided)

> **Proposed default:** Next.js/TypeScript for the web UI · FastAPI/Python for
> HTTP APIs and the existing analysis logic · Supabase Auth + PostgreSQL
> (and Storage) for identity and data.

Recorded as ADR-010, ADR-011, ADR-012 (`DECISIONS.md`). Accept, reject, or
modify before implementation.

```
┌────────────────────────┐        HTTPS / JSON       ┌─────────────────────────┐
│ Next.js (TypeScript)   │ ────────────────────────▶ │ FastAPI (Python)        │
│ App Router             │ ◀──────────────────────── │ /api/v1/*               │
│ Auth via Supabase SDK  │                           │ analyzer_core (pure)    │
└───────────┬────────────┘                           └───────────┬─────────────┘
            │ session (D-4)                                      │ server-side DB role
            ▼                                                    ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ Supabase                                                                     │
│  Auth: email/password, Google, GitHub                                        │
│  PostgreSQL: profiles, datasets, reports — RLS by user_id                    │
│  Storage: uploaded CSVs (optional exports)                                   │
└────────────────────────────────────────────────────────────────────────────┘
```

### 2.1 Proposed roles

| Piece | Role |
|---|---|
| **Web UI — Next.js + TypeScript** | Auth screens, dataset upload/select, report views, history. Does **not** reimplement billing/FSM/trend. |
| **API — FastAPI + Python** | Authn of access tokens, CSV validation, ownership checks, calls `analyzer_core`, persists snapshots. |
| **Identity + store — Supabase** | Email/password + Google + GitHub; Postgres; file storage. |
| **`analyzer_core` (Python)** | INV-1…INV-11 extracted from `server.py` with **no I/O**. Single source of analysis truth. |

### 2.2 Proposed analysis flow

1. Authenticated user uploads CSV or selects a sample.
2. API validates headers (INV-9), stores file + parsed rows, reports invalid rows (INV-10).
3. Run → FastAPI calls `analyze_records` equivalent; persists an **immutable** report snapshot.
4. UI reads the snapshot. Revisit does not recompute. Explicit re-run creates a new report.

### 2.3 Strangler path (keep CLI until D-5)

1. Extract `analyzer_core`; `server.py` becomes a thin TCP shell (behavior-preserving).
2. FastAPI wraps the same core.
3. Next.js consumes FastAPI. TCP client remains until retired.

---

## 3. Proposed data model (PostgreSQL via Supabase)

All user-owned tables carry `user_id` (or a parent FK) with **RLS default-deny**.

| Table | Purpose |
|---|---|
| `auth.users` | Supabase-managed identity |
| `profiles` | Display name / prefs, 1:1 with user |
| `datasets` | Upload or sample metadata, checksum, row counts, status |
| `dataset_rows` | Parsed CSV rows, including invalid ones (negatives stored, flagged) |
| `reports` | Immutable snapshot: metadata + full `result_json` + `engine_version` |
| `report_customers` | Optional denormalization (D-3) |
| `share_links` | Only if D-6 approves |
| `audit_events` | Security-relevant actions, no PII payloads |

Indexes (proposed): `datasets(user_id, created_at desc)`,
`reports(user_id, created_at desc)`, `dataset_rows(dataset_id)`.

---

## 4. Tradeoffs of the proposed default

| Choice | Pros | Cons |
|---|---|---|
| Next.js + TypeScript UI | SSR/RSC, typing, mature auth SDK story | Second runtime (Node) beside Python |
| FastAPI + existing Python engine | Zero rewrite of SymPy/FSM; typed HTTP | Extra service to deploy and observe |
| Supabase Auth + Postgres + Storage | Fast path for three sign-in methods, RLS, files | Vendor coupling; RLS must be tested; residency (D-1) |
| Extract `analyzer_core` | One formula source; CLI + API share tests | Refactor risk (mitigated by goldens) |
| Immutable report snapshots | Stable revisit; audit trail | Storage growth; `engine_version` needed |

### Alternatives (not chosen)

- **A.** Next.js API routes with a TypeScript rewrite of the engine — high drift risk.
- **B.** Django/DRF + templates — one runtime, weaker modern UI defaults.
- **C.** Firebase — weaker relational/report query story.
- **D.** Self-hosted Postgres + custom auth — more control, more security burden.
- **E.** In-browser Python (Pyodide) — no server engine, heavy client, trust issues.

---

## 5. Cross-cutting

- Config via environment; **service-role / DB secrets never in the browser**.
- Structured JSON logs + request IDs; no PII.
- Environments: local → preview → staging → production (hosting is D-1).
- `engine_version` stamped on every report.

## 6. Unresolved architecture decisions

| ID | Topic |
|---|---|
| D-1 | Hosting and data residency (Supabase cloud vs self-hosted Postgres) |
| D-2 | Account-linking across providers |
| D-3 | Whether to denormalize `report_customers` in Phase 1 |
| D-4 | Session strategy: httpOnly cookie BFF vs bearer token in the browser |
| D-5 | Keep or retire the legacy TCP interface |
| D-6 | Export formats and share-link policy |
| D-7 | Charts vs tables in Phase 1 |
| D-8 | Visual/brand direction (`DESIGN.md`) |

API shapes, upload caps, and exact route list are **not** frozen in this phase.
A later backend spec can follow once ADR-010–012 and D-4 are accepted.
