# DECISIONS (ADR log)

Status: Draft · Last updated: 2026-10-18  
Statuses: `accepted` · `proposed` · `unresolved` · `superseded`.

---

## Already in force (existing codebase)

### ADR-000 — Preserve the terminal analyzer’s semantics
- **Status:** accepted
- **Context:** FSM bands, thresholds, TOU, slab, trend, and budget are tested
  course/product behavior.
- **Decision:** INV-1…INV-11 in `PRD.md` are frozen for the web app.
- **Consequences:** Goldens stay green; any numeric change needs a new ADR.

### ADR-001 — TOU and slab remain separate
- **Status:** accepted
- **Context:** `TOU = 4·peak + 2·offpeak`; slab = 3 then 5 after 50 units.
  Grand total in the report is TOU; over-budget uses slab vs Rs 500.
- **Decision:** Compute and display both; never conflate.
- **Consequences:** API/UI always expose `tou_bill` and `slab_bill`.

### ADR-002 — Loopback TCP with explicit double-bind refusal
- **Status:** accepted (legacy runtime)
- **Context:** Windows `SO_REUSEADDR` can hide a second bind.
- **Decision:** Probe and refuse if the port is already served.
- **Consequences:** CLI demo stays safe; not a web-hosting control.

---

## Proposed for the web application (defaults — not accepted)

### ADR-010 — Next.js + TypeScript for the web UI
- **Status:** **proposed (default)**
- **Context:** Need a typed web UI with a strong auth-SDK ecosystem.
- **Decision (proposed):** Next.js App Router + TypeScript.
- **Consequences:** Node toolchain alongside Python.
- **Alternatives:** Remix, SvelteKit, SPA, Django templates.

### ADR-011 — FastAPI (Python) for HTTP APIs
- **Status:** **proposed (default)**
- **Context:** Engine is Python + SymPy; a TypeScript rewrite risks drift.
- **Decision (proposed):** FastAPI calls a pure `analyzer_core`.
- **Consequences:** Second service to deploy; one formula source.
- **Alternatives:** Next.js-only rewrite (rejected as default); Django/DRF;
  calling the TCP server from HTTP (fragile).

### ADR-012 — Supabase Auth + PostgreSQL (+ Storage)
- **Status:** **proposed (default)**
- **Context:** Email/password, Google, GitHub, relational reports, RLS, files.
- **Decision (proposed):** Supabase managed Auth/Postgres/Storage.
- **Consequences:** Vendor coupling; RLS tests mandatory; residency is D-1.
- **Alternatives:** Firebase; Auth0 + self-hosted Postgres; Cognito; fully
  self-hosted Auth.

### ADR-013 — Extract a pure `analyzer_core`; keep the CLI until D-5
- **Status:** **proposed**
- **Context:** Logic is embedded in `server.py`.
- **Decision (proposed):** Move INV-1…INV-11 into a no-I/O module; TCP shell imports it.
- **Consequences:** Enables API + tests + CLI; must be golden-identical.

### ADR-014 — Reports are immutable snapshots
- **Status:** **proposed**
- **Context:** “Revisit saved reports” must not silently change numbers.
- **Decision (proposed):** Persist full result + `engine_version`; re-run inserts a new row.
- **Consequences:** Storage growth; versioning of the result schema.

---

## Unresolved (need a human call)

| ID | Decision | Options | Notes |
|---|---|---|---|
| D-1 | Hosting and data residency | Supabase cloud · self-hosted Postgres · hybrid | Cost, ops, compliance |
| D-2 | Account linking | Link on verified email · keep separate · always prompt | Security-sensitive |
| D-3 | `report_customers` table | Denormalize · JSON snapshot only | Simplicity vs query/compare |
| D-4 | Browser session | httpOnly cookie BFF · bearer token in the SPA | CSRF vs XSS tradeoff |
| D-5 | Legacy TCP interface | Keep (strangler) · retire after web GA | Assignment vs product |
| D-6 | Export and sharing | CSV · PDF · signed read-only link · none in Phase 1 | Injection + privacy |
| D-7 | Charts in Phase 1 | Yes · tables only | Figma shows a 6-bar usage chart `[figma-obs]`; still not accepted |
| D-8 | Visual / brand direction | Accept Figma “Current” · adapt · reject | File **Untitled** fully MCP-inspected 2026-10-18 (`DESIGN.md` §8). Observation ≠ acceptance. |

### Additional product questions (not ADRs yet)

- Password policy details for email sign-up. Figma copy: “Use at least 8 characters.”
  `[figma-obs]` — not an accepted policy.
- Duplicate file uploads: reject vs new dataset.
- Report naming: auto vs user-supplied. Figma uses month titles (“September 2026”).
- Whether `customers_over_budget: ["none"]` stays in the JSON contract for the web API
  or is replaced by `[]` **only after** an ADR (printer currently depends on `"none"`).
- Whether the UI is a **household energy story** (Figma) or the **multi-customer
  analyzer report** (PRD FR-C3). Mixing them without an ADR would hide FSM/slab.
- Figma USD illustration vs locked `Rs` / INV-5–7: **keep analyzer numbers**.
- CSV guide 5 columns vs INV-9 7 columns; `off_peak_units` vs `offpeak_units`.
- Figma “no report if two rows fail” vs INV-10 (analyse valid rows).

## Template

```
### ADR-XXX — <title>
- Status: proposed | accepted | superseded
- Context:
- Decision:
- Consequences:
- Alternatives:
```
