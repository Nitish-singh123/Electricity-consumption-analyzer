# TASKS — Staged work plan

Status: Draft · Last updated: 2026-10-18  
Legend: ✅ done · 🔜 next · ⬜ not started · ⛔ blocked

> **This phase is documentation only. No application code was modified.**

---

## Stage 0 — Discovery and docs (THIS PHASE) ✅

- ✅ Inspect `E:\opencode_projects` (parent, not a git repo) and
  `E:\opencode_projects\app_assignment` (existing git repo).
- ✅ Read README, `server.py`, `client.py`, `tests.py`, `testcases.py`, all three
  CSVs, report pages, committed `outputs/`.
- ✅ Run `python -m unittest -v` (17 tests, OK).
- ✅ Run `python testcases.py all` (TC1–TC3 reports match expected goldens).
- ✅ Create `brain/` packet: PRD, ARCHITECTURE, DESIGN, RULES, TASKS, TEST_PLAN,
  SECURITY, DECISIONS, MEMORY.
- ✅ Phase 0 audit: re-ran suite + three test cases; labeled `docs/BACKEND_SPEC.md` as Figma-draft; added `.cursor/rules` (no duplicate Brain packet).
- Exit: docs describe the as-is app; baseline recorded from this run; no app edits.

---

## Stage 1 — Extract the analysis core (no behavior change) 🔜

Depends on: review of Stage 0 docs (this packet).

- ⬜ Extract INV-1…INV-11 from `server.py` into a pure `analyzer_core` (or equivalent).
- ⬜ Keep `server.py` as a thin TCP shell importing the core.
- ⬜ Add `pyproject.toml`; declare `sympy` and test deps.
- ⬜ Add `.gitignore`; stop tracking `__pycache__`.
- ⬜ Keep the existing 17 tests green; add/retain TC1–TC3 goldens.
- Exit: same numbers as Stage 0 baseline; TCP CLI still works.
- Risk: refactor drift — mitigated by goldens.

## Stage 2 — HTTP API (FastAPI) ⬜

Depends on: Stage 1 and proposed ADR-011.

- ⬜ Analyze endpoint wrapping `analyzer_core` with typed models.
- ⬜ Validation limits; safe error envelope (do not echo raw exceptions to clients).
- ⬜ Health check; structured logs + request IDs.
- ⬜ Contract tests against goldens.
- Exit: HTTP path reproduces TC1–TC3.

## Stage 3 — Identity (Supabase Auth) ⬜

Depends on: ADR-012 proposed default; **D-2** and **D-4** should be decided first.

- ⬜ Email/password sign-up, verification, reset.
- ⬜ Google OAuth.
- ⬜ GitHub OAuth (handle missing/private email).
- ⬜ Session + logout-everywhere per D-4.
- Exit: all three methods work; auth tests green.

## Stage 4 — Datasets (upload + storage) ⬜

Depends on: Stage 3.

- ⬜ `datasets` + `dataset_rows` + migrations + RLS.
- ⬜ CSV upload validation (INV-9 / INV-10); size and row caps.
- ⬜ Bundled samples selectable.
- ⬜ Preview + invalid-row reporting.
- Exit: isolation tests pass; invalid rows do not crash analysis.

## Stage 5 — Reports (persist + revisit) ⬜

Depends on: Stages 2 and 4; ADR-014.

- ⬜ Immutable `reports` snapshots (`result_json`, `engine_version`) + RLS.
- ⬜ Save on run; list; open snapshot; explicit re-run creates a new report.
- ⬜ Report UI content per `DESIGN.md` §6 (visuals still undecided).
- ⬜ Export only after D-6.
- Exit: reopen matches snapshot; lists are user-scoped.

## Stage 6 — Web UI (Next.js) ⬜

Depends on: Stages 3–5; **D-8 / DESIGN.md visual slots still open** — do not
invent a brand. Use a temporary unstyled/accessible shell until design is chosen.

- ⬜ Auth screens, dashboard, dataset flow, report views.
- ⬜ Accessibility pass (WCAG 2.1 AA targets).
- Exit: sign-in → upload/select → analyse → revisit works end to end.

## Stage 7 — Security hardening and observability ⬜

- ⬜ Rate limits, security headers, CSRF strategy matching D-4, secret management.
- ⬜ RLS test suite in CI; SCA/SAST.
- ⬜ No-PII logging validated.
- Exit: `SECURITY.md` checklist for Phase 1.

## Stage 8 — Deployment and operations ⬜

Depends on: D-1.

- ⬜ Environments; CI/CD; backups; rollback.
- ⬜ Performance smoke (NFR-3 still a target until measured).
- Exit: documented deploy + rollback.

---

## Icebox (not scheduled)

- Multi-dataset comparison.
- Share links (if D-6).
- Budget-breach notifications.
- Alternate utility CSV formats.
- Configurable currency/rates (would need an ADR; default rates stay INV-5/6).
- Retire TCP interface (D-5).

## Dependency graph

```
Stage 0 ✅ → Stage 1 → Stage 2 ─┐
                    Stage 3 → Stage 4 ─┴→ Stage 5 → Stage 6 → Stage 7 → Stage 8
```

Stage 3 is ⛔ for account linking and session details until D-2 and D-4 are called.
Stage 6 is ⛔ for visual polish until D-8.
