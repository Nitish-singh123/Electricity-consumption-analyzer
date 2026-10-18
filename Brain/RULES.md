# RULES — Engineering, domain, and process

Status: Draft · Last updated: 2026-10-18  
Binding for humans and AI agents in this repository. To break a rule, write an
ADR in `DECISIONS.md` first.

---

## 1. Domain invariants (highest priority)

- R-1 Never change analysis semantics silently. INV-1…INV-11 in `PRD.md` are frozen.
- R-2 TOU and slab stay distinct. Report both; never merge or substitute.
- R-3 Thresholds are exact: high-usage `>= 20`; FSM edges 10 / 20 / 30; budget
  Rs 500; slab limit 50; TOU rates 4 (peak) and 2 (off-peak).
- R-4 The web app must reproduce the goldens in `PRD.md` §7.
- R-5 CSV schema is `record_id, customer_id, customer_name, date, day_index, peak_units, offpeak_units`.
- R-6 Invalid records (missing or negative readings) are excluded from totals
  and counted — the request must not crash.
- R-7 Over-budget uses **slab** (`bill_amount(total_units) > 500`), not TOU.

## 2. Source of truth and change control

- R-8 Read existing code before changing it. `server.py` / `client.py` /
  `tests.py` / `testcases.py` are the behavioral reference.
- R-9 Product/process docs for this effort live in `brain/` (this packet).
  Update `MEMORY.md` at the end of each phase.
- R-10 Keep analysis formulas in **one** module once extracted. No copy-paste
  of rates or slab logic into the UI or exporters.
- R-11 Do not modify application code in a documentation-only phase.

## 3. Code quality (when implementation starts)

- R-12 Python: formatter + linter; type hints on public functions of the core
  and API.
- R-13 TypeScript: `strict: true`; no unexplained `any`.
- R-14 Core analysis has **no I/O and no network**.
- R-15 No new runtime dependency without a short justification (PR or ADR).

## 4. Testing

- R-16 Behavior changes ship with tests; bug fixes ship with a regression test.
- R-17 TC1 / TC2 / TC3 goldens run in CI and must stay green.
- R-18 Authorization: a user must never read another user’s datasets or reports.
- R-19 Never claim “tests passed” without running them and recording the result.

## 5. Security and privacy

- R-20 Never commit secrets, tokens, or real personal data.
- R-21 Bound all uploads (size, rows, encoding) and JSON bodies.
- R-22 Safe-encode exports (CSV formula injection, HTML escaping).
- R-23 Log without PII; never log raw CSV contents or tokens.
- R-24 Least privilege: browser holds only the public anon key + user session.

## 6. Data

- R-25 Schema changes are versioned migrations.
- R-26 Every user-owned table has RLS enabled and an isolation test.
- R-27 Reports are immutable snapshots; a re-run creates a new report.
- R-28 User/dataset deletion cascade is documented in the migration.

## 7. Honesty

- R-29 Do not invent metrics, screenshots, or test outcomes.
- R-30 State assumptions explicitly.
- R-31 Required CI checks are not silently skipped.

## 8. Definition of Done (per implementation task)

1. Types/lint clean for touched code.
2. Tests added/updated and green locally; goldens unchanged unless an ADR says otherwise.
3. Security implications considered.
4. `TASKS.md` / `MEMORY.md` updated; ADR if a rule changed.
5. Stop at the requested phase boundary.

## 9. AI-assistant working rules

- R-32 Inspect before editing; do not rewrite unrelated files.
- R-33 Stay inside the requested phase scope.
- R-34 Prefer small, reviewable diffs.
- R-35 The vibe-coding guide is process inspiration only. Do not import sample
  product features or sample tech choices as requirements.
