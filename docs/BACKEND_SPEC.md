# BACKEND_SPEC — Electricity Consumption Analyzer (Web)

Status: **Draft / assumptions-heavy** · Last updated: 2026-10-18  
**Phase 0:** this file is **not** an approved product spec. Visual design is **not accepted**
(`Brain/DESIGN.md` D-8) even though Figma was fully MCP-inspected. Do not implement from
Figma-derived screens, copy, or tokens until the owner selects a direction.

Precedence (must win over this draft):
1. Cursor chat instructions
2. Behavior in `server.py` / `client.py` / `tests.py` / datasets
3. `Brain/DECISIONS.md` and `Brain/PRD.md`
4. Other Brain docs
5. **This file** — API/schema ideas may be reused later; Figma inventory is `[figma-obs]`, not UX law

What **is** evidence-backed here: INV checklist and analysis JSON contract (`[code]`), matching
`Brain/PRD.md`. What is **not**: approved UI. Figma uses USD household mocks; the analyzer uses
`Rs` and INV-5…INV-7. Illustration numbers are **never** report data.

Sources of truth used:
- **Calculations/behaviour:** `server.py`, `client.py`, `tests.py`, `testcases.py`, `README.md`,
  `dataset.csv`, `dataset_high.csv`, `dataset_edge.csv` (unchanged — see §0.3).
- **Phase 0 docs:** `Brain/PRD.md`, `Brain/ARCHITECTURE.md`, `Brain/DESIGN.md`, `Brain/DECISIONS.md`,
  `Brain/RULES.md`, `Brain/SECURITY.md`, `Brain/TEST_PLAN.md`, `Brain/TASKS.md`, `Brain/MEMORY.md`.
- **Design (UNAPPROVED, MCP-inspected):** [Untitled](https://www.figma.com/design/QpIaPoDpZVCS2jno7Gn6Nk/Untitled?node-id=0-1)
  — all 15 frames screenshot-inspected. Full visual notes live in `Brain/DESIGN.md` §8.

> **Legend:** `[figma-obs]` / `[obs]` = MCP screenshot + layer structure ·
> `[inf]` = inference · `[code]` = analyzer · `[unknown]` = prototype/hover/keyboard not exposed.

---

## 0. How this spec was derived

### 0.1 Figma access (updated 2026-10-18)
Figma MCP **is connected** in Cursor (`whoami` + `get_metadata` + `get_design_context` with
screenshots). File key `QpIaPoDpZVCS2jno7Gn6Nk`, page **Page 1**, document name **Untitled**.

All **15** top-level frames were visually inspected (screenshot viewed), including the 13 that
were remaining after Sign in · Desktop and Foundations. Named variables on Foundations
returned `{}`. Prototype/motion was **not** confirmed (`get_motion_context` interrupted) —
interactions stay `[unknown]`.

Earlier drafts of this file that said “no MCP / browser-only / unreadable copy” are **superseded**.
Token and copy details are in `Brain/DESIGN.md` §8.

### 0.2 Scope discipline
Sections 1–2 inventory a **Figma draft**. They are **not** Phase 0 requirements. Product
behavior is INV-1…INV-11 in `Brain/PRD.md`. `[figma-obs]` stays unaccepted until D-8.

### 0.3 Existing analyzer is unchanged
No file outside `docs/` was created or modified in this phase. The analyzer, tests and datasets are
untouched; calculations below are quoted from the current code and are the authority.

---

## 1. Figma screen inventory and the user actions each supports

The file contains **15 frames** `[figma-obs]`, grouped into four families. Copy below is
from MCP, not inferred. **USD / 420 kWh / $109.20 / $130 budget / $20.80** are sample
illustration only.

| # | Frame `[figma-obs]` | Node | Family | Purpose |
|---|---|---|---|---|
| 1 | **Sign in · Desktop** | `2:11990` | Auth | Email/password + Google/GitHub (split layout) |
| 2 | **Sign in · Mobile** | `2:12058` | Auth | Same form; no welcome panel |
| 3 | **Sign up · Desktop** | `2:12099` | Auth | OAuth first, then name/email/password |
| 4 | **Sign up · Mobile** | `2:12176` | Auth | Same, stacked |
| 5 | **Dashboard · Desktop** | `2:12226` | App | Home: latest month, 3 cards, 3 reports |
| 6 | **Dashboard · Mobile** | `2:12335` | App | Same, stacked + bottom nav |
| 7 | **Upload dataset · Desktop** | `2:12425` | App | Drop CSV; 5-column guide; Rowan House sample |
| 8 | **Upload dataset · Mobile** | `2:12541` | App | Browse-first |
| 9 | **Analysis results · Desktop** | `2:12648` | App | Household report mock |
| 10 | **Analysis results · Mobile** | `2:12779` | App | Same; no third key-figure card |
| 11 | **Dashboard · Desktop · New account** | `2:12899` | Empty | First-run |
| 12 | **Dashboard · Mobile · New account** | `2:12950` | Empty | First-run; 3 step rows |
| 13 | **Account feedback · Validation and verification** | `2:13005` | Feedback | 4 auth states |
| 14 | **Upload feedback · Progress, success and errors** | `2:13072` | Feedback | 3 upload states |
| 15 | **Current · Foundations and patterns** | `2:13139` | System | Tokens (see DESIGN §8.2) |

### 1.1 Sign in · Desktop `[figma-obs]`
Split layout: 500 px **Welcome panel** (`#F0F5FC`) + form.

- Brand **current**; “Less guessing. / More clarity.”; card **420 kWh in September**; six bars;
  chip **“$20.80 under budget”** (sample USD); “Your data stays in your account.”
- Form: “Need help?” · “Welcome back” · “Sign in to understand your energy use.” · Email
  `you@example.com` · Password + `eye-off` · **Forgot password?** · **Sign in** · “or continue with”
  **Continue with Google / GitHub** · “New to Current? **Create an account**” · Privacy · Terms.
- Prototype destinations `[unknown]`.

### 1.2 Sign in · Mobile `[figma-obs]`
Same form; welcome panel omitted; brand in header; title 27 px; padding 24 px. No “Need help?”.

### 1.3 Sign up · Desktop `[figma-obs]`
Same welcome panel (including **$20.80 under budget** sample). Form: “Make sense of your energy” /
“Create your free Current account.” **Sign up with Google/GitHub first**, then “or use your email.”
Name, Email, Password (hint **Use at least 8 characters.**), Confirm password. Verification email
note. **Create account**. “Already have an account? **Sign in**”. Privacy · Terms.

### 1.4 Sign up · Mobile `[figma-obs]`
Same fields as desktop; no welcome panel.

### 1.5 Dashboard · Desktop `[figma-obs]`
Header: **current · Electricity analyzer**; nav **Dashboard / Datasets / Reports / Settings**
(Dashboard active); avatar **AM**. “Hello, Alex” / “Your latest month, at a glance.” **Upload a
dataset**. Context “Rowan House · 1–30 September 2026” · “Latest report”. Cards: **420 kWh**
(252 peak · 168 off-peak); **$109.20** (“Illustrative rates, not a utility bill”); **On track**
(“$20.80 left of your $130 budget”). Recent reports ×3 (Sep/Aug/Jul 2026) with **View report**.
Footnote `$0.30` peak / `$0.20` off-peak. Footer Help. Datasets/Reports/Settings screens **not drawn**.

### 1.6 Dashboard · Mobile `[figma-obs]`
Same numbers; upload full-width under heading; cards stacked; compact report rows; bottom nav;
no table headers; no footer Help.

### 1.7 Upload dataset · Desktop `[figma-obs]`
Back “Dashboard”. “Upload your dataset”. Steps **1 Upload** (active) · 2 Check file · 3 View report.
Drop: “Drag and drop your CSV here” · Browse files · “CSV only · Up to 10 MB”. Guide: **five**
headers `customer_id`, `customer_name`, `date`, `peak_units`, **`off_peak_units`**. Sample:
Rowan House 30 days · Try sample data · Download sample CSV. See §5.1 mismatch with INV-9.

### 1.8 Upload dataset · Mobile `[figma-obs]`
Browse-first (“Choose your CSV file”); drag mentioned as extra. Columns stacked (date shows
YYYY-MM-DD on the row). Datasets nav active. Bottom nav.

### 1.9 Analysis results · Desktop `[figma-obs]`
Household mock — **not** the analyzer’s multi-customer report. Breadcrumb Reports / September 2026.
“Your September energy report” · “Report ready”. Summary uses **420 kWh / $109.20 / $20.80 / $130**.
Three cards (usage, estimated bill, **14 kWh** daily average for C001). Layer **“Editable usage
chart”**: six 5-day bars; **no edit controls visible**. Bill lines: 252 kWh × **$0.30** = $75.60;
168 kWh × **$0.20** = $33.60; total $109.20. Budget 84% of $130. Source
`rowan-house-sep-2026.csv`. Missing vs PRD FR-C3: FSM, slab, TOU-as-Rs, ranking, high-usage, trend.

### 1.10 Analysis results · Mobile `[figma-obs]`
Same bill/budget/chart; two key-figure cards (daily average folded into usage caption); bottom
nav Reports active.

### 1.11–1.12 New-account dashboards `[figma-obs]`
“Welcome, Alex” · empty “Your energy story starts here” · Upload a dataset · Try sample data ·
“CSV files up to 10 MB”. Desktop: one combined step line. Mobile: three rows (Upload / Check /
Understand).

### 1.13 Account feedback `[figma-obs]`

| State | Visible copy | Backend meaning `[inf]` |
|---|---|---|
| Sign in / Field validation | “Check your details”; `alex@` → enter a full email; empty password | Client validation |
| Sign in / Account error | “The email or password isn’t right.” + Forgot password? + Try again | Generic auth failure (S-6) |
| Sign up / Field validation | “Almost there”; ≥8 characters; “Passwords don’t match.” | Policy + mismatch |
| Sign up / Verification sent | “Check your inbox” to alex@example.com; Back to sign in; Resend | Confirm email before use |

### 1.14 Upload feedback `[figma-obs]`

| State | Visible copy | Backend meaning `[inf]` |
|---|---|---|
| In progress | `rowan-house-sep-2026.csv` 4.2 KB; **64%**; Cancel upload | Transfer in flight |
| Success | “All 30 readings passed our checks.” · 420 kWh · View analysis | Parsed OK |
| Validation error | “2 rows need attention” · **“No report has been created.”** · Row 12 date missing · Row 19 peak −4 · Choose corrected file | **Conflicts with INV-10** (valid rows should still analyse) `[code]` |

### 1.15 Foundations `[figma-obs]`
Tokens and patterns: `DESIGN.md` §8.2. Palette hexes now known. Inter; spacing 4–48; 10 px
controls; 16 px cards; desktop 1280 / 88 px; mobile 390 / 20 px.

---

## 2. Screen-to-data and screen-to-API mapping

### 2.1 Analysis result contract (unchanged authority — `server.py` `[code]`)
Every report screen is a rendering of the existing result object:

```
{
  records_received, records_analyzed, records_invalid,
  invalid_records[], billed_records[], high_usage_records[],
  customers[ { rank, customer_id, customer_name, days, daily_units[],
               fsm_path[], final_state, recommendation,
               total_units, tou_bill, slab_bill,
               trend_a, trend_b, trend_equation, predicted_next_day_units } ],
  summary { customers, total_units, total_tou_bill, average_units_per_record },
  budget  { monthly_budget: 500.0, max_units_allowed: 120.0, customers_over_budget[] }
}
```
`[code]` Key constants: FSM bands `<10 / 10–19 / 20–29 / ≥30` → `LT10/B10_19/B20_29/GE30`
(INV-1); states `LOW/MODERATE/HIGH/OVERLOAD` (INV-2); next state = band's state (INV-3);
high-usage `total_units ≥ 20` (INV-4); **TOU** `peak×4 + offpeak×2` (INV-5); **slab**
`3x` if `x≤50` else `150+5(x−50)` (INV-6); budget `Rs 500` → `120` units (INV-7);
least-squares trend, predict day `n+1` (INV-8); CSV schema (INV-9); invalid = missing/negative
reading, excluded from totals (INV-10); **TOU and slab are reported separately and never conflated** (INV-11).

### 2.2 Analysis results screen → data → API

| Design element `[obs]` | Data field `[inf]` | Endpoint |
|---|---|---|
| Report header title/description | report name, dataset name, created_at | `GET /api/v1/reports/{id}` |
| Report status (dot + label) | dataset/report status, or the report's dominant `final_state` | `GET /api/v1/reports/{id}` |
| Plain-language summary | `recommendation` (aggregate) / report summary text | `GET /api/v1/reports/{id}` |
| Key figure 1 (`zap`) | `summary.total_units` | `GET /api/v1/reports/{id}` |
| Key figure 2 (`wallet`) | `summary.total_tou_bill` **and** aggregate slab (`tou_bill`/`slab_bill` per customer) | `GET /api/v1/reports/{id}` |
| Key figure 3 (`calendar-days`) | period (first/last date, `days`) | `GET /api/v1/reports/{id}` |
| Consumption trend bars + date labels | `daily_units[]` + `date[]` (+ `predicted_next_day_units`, `trend_equation` for the line) | `GET /api/v1/reports/{id}` (series embedded) |
| Bill line 1 / line 2 | Figma `[figma-obs]` is peak×$0.30 and off-peak×$0.20 (sample). Product `[code]` must remain INV-5 TOU and INV-6 slab as **separate** figures — do not bind USD mock rates | `GET /api/v1/reports/{id}` |
| Estimated total | Figma `$109.20` is sample. Product: `summary.total_tou_bill` in **Rs**; never merge slab | `GET /api/v1/reports/{id}` |
| Budget remaining (amount + description) | `budget.monthly_budget` − spend, `budget.max_units_allowed` | `GET /api/v1/reports/{id}` |
| Budget meter (used) | budget utilisation | `GET /api/v1/reports/{id}` |
| (per-customer ranking, FSM path, final state, recommendation, trend, prediction) | `customers[]` (PRD FR-C3) | `GET /api/v1/reports/{id}` |
| (high-usage list, INV-4) | `high_usage_records[]` | `GET /api/v1/reports/{id}` |

### 2.3 Dashboard screen → data → API

| Design element `[obs]` | Data field `[inf]` | Endpoint |
|---|---|---|
| Latest dataset context: period + status | `datasets.first_date/last_date`, `status` | `GET /api/v1/datasets?limit=1` |
| Monthly summary card 1 (`zap`) | latest report `summary.total_units` | `GET /api/v1/reports?limit=1` |
| Monthly summary card 2 (`wallet`) | latest report `summary.total_tou_bill` | `GET /api/v1/reports?limit=1` |
| Monthly summary card 3 (`circle-check`) | latest report budget state (`customers_over_budget`) | `GET /api/v1/reports?limit=1` |
| Recent reports (report count + rows: title, date, created, Usage, Estimated bill) | `reports[]` (id, name, dataset, created_at, total_units, total_tou_bill) | `GET /api/v1/reports?limit=N` |
| "View report" action | report id | `GET /api/v1/reports/{id}` |
| Empty state (#11/#12) | `reports`/`datasets` empty | `GET /api/v1/reports` returns `[]` |

### 2.4 Upload screen → API

| Design element `[obs]` | Backend | Endpoint |
|---|---|---|
| Drag-drop / Browse files | multipart upload | `POST /api/v1/datasets` |
| Upload steps (3) | client progress; server job status | `GET /api/v1/upload-jobs/{id}` (optional, §3.7) |
| Upload in progress (percentage) | job progress | `GET /api/v1/upload-jobs/{id}` |
| Cancel upload | abort job / discard file | `DELETE /api/v1/upload-jobs/{id}` |
| Validated dataset summary (rows/cols + status) | validation summary | `POST /api/v1/datasets` response |
| CSV validation error + **validation issues (row issues)** | structured `issues[]` | `POST /api/v1/datasets` (422/202) |
| Choose corrected file | re-upload | `POST /api/v1/datasets` |
| View analysis | run the engine | `POST /api/v1/datasets/{id}/analyses` |
| Try sample data | instantiate bundled sample | `POST /api/v1/samples/{sample_id}/datasets` |
| Download sample link | download bundled CSV | `GET /api/v1/samples/{sample_id}` |

### 2.5 Auth screens → API

| Design element `[obs]` | Supabase call `[inf]` | Notes |
|---|---|---|
| Sign in (email+password) | `signInWithPassword` | Sets session |
| Continue with Google | `signInWithOAuth({provider:'google'})` | Redirect flow |
| Continue with GitHub | `signInWithOAuth({provider:'github'})` | Redirect flow |
| Create account | `signUp` | Sends verification e-mail |
| Required-field validation state | client + `POST /api/v1/account` (`422`) | `[inf]` |
| Incorrect credentials state | Supabase `invalid_credentials` | Mapped to safe message |
| Sign up · Password validation | password policy | `[inf]` policy in Q9 |
| Email verification sent / Resend | Supabase confirmation + `resend` | Design has "Resend verification email" |
| Back to sign-in / recovery link | `resetPasswordForEmail` | `[inf]` |
| Account → Initials | `GET /api/v1/me` → `profiles.display_name` | `[inf]` |

---

## 3. Proposed PostgreSQL schema (Supabase-managed)

Conventions: UUID PKs (`gen_random_uuid()`), `created_at`/`updated_at` `timestamptz`,
money `numeric(12,2)`, units `numeric(14,3)`, `Rs` implied. RLS **on for every table**.

### 3.1 `profiles` (1:1 with `auth.users`)
| Column | Type | Constraints |
|---|---|---|
| `id` | uuid | **PK**, FK → `auth.users(id)` `on delete cascade` |
| `display_name` | text | null; length ≤ 120 |
| `initials` | text | generated/derived (dashboard avatar) |
| `created_at`, `updated_at` | timestamptz | not null, default `now()` |

Ownership: `id = auth.uid()`. Created by a trigger on `auth.users` insert (no client insert).

### 3.2 `datasets`
| Column | Type | Constraints |
|---|---|---|
| `id` | uuid | PK |
| `user_id` | uuid | **not null**, FK → `auth.users(id)` `on delete cascade` |
| `name` | text | not null, ≤ 200 |
| `source` | text | not null, `check in ('upload','sample')` |
| `original_filename` | text | null (upload only) |
| `storage_path` | text | null (Supabase Storage key) |
| `file_size_bytes` | bigint | `check (file_size_bytes >= 0)` |
| `checksum_sha256` | text | null; dedupe/idempotency |
| `rows_total` | int | not null, `>= 0` |
| `rows_valid` | int | not null, `>= 0`, `<= rows_total` |
| `rows_invalid` | int | not null, `>= 0` |
| `columns_detected` | text[] | header actually found |
| `first_date`, `last_date` | date | null; from rows |
| `status` | text | not null, `check in ('validating','ready','invalid')` |
| `created_at` | timestamptz | not null |

Indexes: `(user_id, created_at desc)`. Unique `(user_id, checksum_sha256)` **nullable** → optional
dedupe (Q10).

### 3.3 `dataset_rows`
| Column | Type | Constraints |
|---|---|---|
| `id` | bigint identity | PK |
| `dataset_id` | uuid | not null, FK → `datasets(id)` `on delete cascade` |
| `row_number` | int | not null (1-based data row, for error reporting) |
| `record_id` | int | null (raw) |
| `customer_id` | text | null |
| `customer_name` | text | null |
| `date` | date | null (raw string also kept when unparseable, `raw_date text`) |
| `day_index` | int | null |
| `peak_units` | numeric(14,3) | null (**may be negative — see §5.2**) |
| `offpeak_units` | numeric(14,3) | null |
| `is_valid` | boolean | not null |
| `invalid_codes` | text[] | not null default `'{}'` |

Indexes: unique `(dataset_id, record_id)` where `record_id is not null`; `(dataset_id, is_valid)`.
> **Deliberate:** no `check (peak_units >= 0)` — negative values must be *stored and reported* as
> invalid rows (INV-10, design state #14), not rejected by the database.

### 3.4 `reports` (immutable snapshot — ADR-014)
| Column | Type | Constraints |
|---|---|---|
| `id` | uuid | PK |
| `user_id` | uuid | not null, FK → `auth.users(id)` `on delete cascade` |
| `dataset_id` | uuid | not null, FK → `datasets(id)` `on delete cascade` |
| `name` | text | not null (dashboard "report title") |
| `engine_version` | text | **not null** |
| `created_at` | timestamptz | not null (dashboard "created date") |
| `period_start`, `period_end` | date | null |
| `records_received`, `records_analyzed`, `records_invalid` | int | not null, `>= 0` |
| `customers_count` | int | not null |
| `total_units` | numeric(14,3) | not null |
| `total_tou_bill` | numeric(12,2) | not null |
| `average_units_per_record` | numeric(14,3) | not null |
| `monthly_budget` | numeric(12,2) | not null default 500.00 |
| `max_units_allowed` | numeric(14,3) | not null |
| `customers_over_budget` | text[] | not null |
| `result_json` | jsonb | not null — the **full** contract in §2.1 |

Indexes: `(user_id, created_at desc)`, `(dataset_id)`.
**Write-once:** no `UPDATE` policy; only `INSERT`/`SELECT` (+ `DELETE` by owner).

### 3.5 `report_customers` (queryable denormalisation — Open Decision D-3)
| Column | Type | Constraints |
|---|---|---|
| `id` | bigint identity | PK |
| `report_id` | uuid | not null, FK → `reports(id)` `on delete cascade` |
| `rank` | int | not null |
| `customer_id`, `customer_name` | text | not null |
| `days` | int | not null |
| `total_units` | numeric(14,3) | not null |
| `tou_bill`, `slab_bill` | numeric(12,2) | not null (**kept separate — INV-11**) |
| `final_state` | text | not null, `check in ('LOW','MODERATE','HIGH','OVERLOAD')` |
| `trend_a`, `trend_b` | numeric(14,4) | not null |
| `trend_equation` | text | not null |
| `predicted_next_day_units` | numeric(14,2) | not null |
| `daily_units` | jsonb | not null (§2.1 order = by `day_index`) |
| `fsm_path` | jsonb | not null |

Unique `(report_id, customer_id)`; index `(report_id, rank)`.

### 3.6 `report_series` (chart source) `[inf]`
`(report_id, day_index, date, total_units, peak_units, offpeak_units)` aggregated per day for the
consumption-trend chart. Optional if the chart is rendered from `result_json` — Q12.

### 3.7 Supporting tables (optional, Phase 1)
- `upload_jobs` `[inf]` — `id, user_id, dataset_id, status ('pending'|'running'|'succeeded'|'failed'|'cancelled'), progress_pct, error jsonb, created_at, finished_at`; drives the "In progress / Cancel" states.
- `report_invalid_rows` `[inf]` — mirrors `invalid_records[]` for the report's invalid-row details.
- `share_links` — per ADR/D-6, if approved.
- `audit_events` — security-relevant actions, **no PII payloads**.

### 3.8 Relationship summary
```
auth.users 1─1 profiles
auth.users 1─* datasets 1─* dataset_rows
auth.users 1─* reports  *─1 datasets
reports    1─* report_customers
reports    1─* report_series
auth.users 1─* upload_jobs
```

### 3.9 Per-user ownership rules
1. Every user-owned table carries `user_id` (directly, or transitively via `dataset_id`/`report_id`).
2. RLS `SELECT/INSERT/UPDATE/DELETE` policy: `user_id = auth.uid()`; child tables use
   `exists (select 1 from parent p where p.id = <fk> and p.user_id = auth.uid())`.
3. `reports` has **no UPDATE** policy (immutability).
4. Storage objects are namespaced `/{user_id}/...` with storage RLS matching `auth.uid()`.
5. The API **derives** `user_id` from the verified token `sub`; a body-supplied `user_id` is ignored.

---

## 4. API routes (FastAPI)

Base: `/api/v1`. Auth: `Authorization: Bearer <supabase access token>` (all routes except
`/health`). Every request is scoped to the token's `sub`.

**Error envelope** (all non-2xx):
```json
{ "error": { "code": "MISSING_COLUMNS", "message": "Human-readable summary",
             "details": { "...": "structured, safe" }, "request_id": "..." } }
```
Codes: `UNAUTHENTICATED` (401), `FORBIDDEN` (403), `NOT_FOUND` (404), `VALIDATION_ERROR` (422),
`FILE_TOO_LARGE` (413), `UNSUPPORTED_MEDIA_TYPE` (415), `RATE_LIMITED` (429), `CONFLICT` (409),
`INTERNAL` (500).

### 4.1 Identity
| Method | Path | Request | Response 2xx | Errors |
|---|---|---|---|---|
| GET | `/me` | — | `{ id, email, display_name, initials, providers[] }` | 401 |
| PATCH | `/me` | `{ display_name }` | same as GET | 400/401/422 |
| POST | `/account/sync` | — | 204 — ensures `profiles` row exists | 401 |

> Sign-in/sign-up/OAuth/verification/reset are performed by the **Supabase SDK** against Supabase
> Auth; the API only **verifies** tokens (§6). `/account/sync` is idempotent and optional if a DB
> trigger creates `profiles`.

### 4.2 Datasets
| Method | Path | Request | Response 2xx | Errors |
|---|---|---|---|---|
| GET | `/datasets` | `?limit&cursor` | `{ items:[{id,name,source,rows_total,rows_valid,rows_invalid,first_date,last_date,status,created_at}], next_cursor }` | 401 |
| POST | `/datasets` | multipart `file` (+ `name?`) | **201** `{ dataset:{…}, validation:{…} }` (§5.3) | 400/401/409/413/415/422 |
| POST | `/datasets` | JSON `{ source:"sample", sample_id }` | 201 same | 400/404/422 |
| GET | `/datasets/{id}` | — | dataset detail + `validation` summary | 401/403/404 |
| GET | `/datasets/{id}/rows` | `?valid_only&limit&cursor` | `{ items:[{row_number,record_id,customer_id,customer_name,date,day_index,peak_units,offpeak_units,is_valid,invalid_codes}], next_cursor }` | 401/403/404 |
| GET | `/datasets/{id}/issues` | `?limit&cursor` | `{ items:[ row issue ] }` (drives state #14) | 401/403/404 |
| DELETE | `/datasets/{id}` | — | 204 | 401/403/404 |

### 4.3 Samples
| Method | Path | Response | Errors |
|---|---|---|---|
| GET | `/samples` | `{ items:[{id,name,description,rows,customers}] }` (`dataset.csv`, `dataset_high.csv`, `dataset_edge.csv` — INV/README `[code]`) | 401 |
| GET | `/samples/{id}` | the bundled CSV (safe `Content-Disposition: attachment`) | 401/404 |
| POST | `/samples/{id}/datasets` | 201 as §4.2 (creates a user-owned dataset copy) | 401/404 |

### 4.4 Reports
| Method | Path | Request | Response 2xx | Errors |
|---|---|---|---|---|
| GET | `/reports` | `?limit&cursor&dataset_id` | `{ items:[{id,name,dataset_id,created_at,total_units,total_tou_bill,customers_count,period_start,period_end}], next_cursor }` | 401 |
| POST | `/datasets/{id}/analyses` | `{ name? }` | **201** `{ report: <full §2.1 result + meta> }` | 401/403/404/**422 NO_VALID_ROWS** |
| GET | `/reports/{id}` | — | `{ report:{…}, customers:[…], series:[…], meta:{engine_version,created_at} }` | 401/403/404 |
| DELETE | `/reports/{id}` | — | 204 | 401/403/404 |
| POST | `/reports/{id}/rerun` | — | 201 — new report from the same dataset | 401/403/404/409 |
| GET | `/reports/{id}/export` | `?format=csv` | file (`attachment`, formula-injection-safe per `SECURITY.md`) | 401/403/404/406 |

> `POST /datasets/{id}/analyses` may be **synchronous** (design's "View analysis" is a step, and the
> 3 upload steps imply a prepare→upload→analyse flow). For ≤10k rows the engine runs well under 2 s
> (NFR-3). A `job_id` variant is available if the UI wants the progress states (§3.7, Q8).

### 4.5 Upload jobs (optional — only if uploads are async)
`GET /upload-jobs/{id}` → `{ status, progress_pct, error? }` · `DELETE /upload-jobs/{id}` → 204 (cancel).

### 4.6 Health
`GET /health` → `{ status:"ok", engine_version, db:"ok" }` (no auth).

### 4.7 Cross-cutting API rules
- Idempotency: `POST /datasets` honours `Idempotency-Key` (or `checksum_sha256`) to avoid duplicates.
- Rate limits: per-user on `POST /datasets` and `.../analyses` (design's progress states + NFR).
- Pagination: opaque cursor, default 20, max 100.
- All responses omit another user's data — enforced by RLS **and** an explicit ownership check.

---

## 5. CSV upload validation and invalid-row reporting

### 5.1 Required headers
`[code]` INV-9: `record_id, customer_id, customer_name, date, day_index, peak_units, offpeak_units`
(type rules from `client.py load_dataset` `[code]`: `record_id`→int, `customer_id`/`customer_name`→
trimmed str, `date`→`YYYY-MM-DD` str, `day_index`→int, `peak_units`/`offpeak_units`→float).

> ⚠️ **Mismatch to resolve (Q3):** Figma guide `[figma-obs]` lists **five** headers:
> `customer_id`, `customer_name`, `date`, `peak_units`, **`off_peak_units`**. INV-9 `[code]`
> requires **seven**: `record_id`, `customer_id`, `customer_name`, `date`, `day_index`,
> `peak_units`, **`offpeak_units`** (no underscore). **Backend still requires all 7 unless
> you file an ADR.** Also: Figma examples use `C001` / Alex Morgan; goldens use C01–C11.

### 5.2 Validity rules (must reproduce INV-10 exactly)
- **Row-level invalid (excluded, counted, reported — analysis still runs):** a reading is missing or
  negative (`peak_units < 0` or `offpeak_units < 0` or absent) → mirrors `is_valid()` `[code]`.
  Example: `dataset_edge.csv` row `C11` `peak=-5.0` → "10 received / 9 analyzed / 1 invalid" `[code]`.
- **File-level blocking (no dataset created):** missing/duplicate/unknown required header,
  no parseable rows at all, empty file, over size/row caps, non-CSV/non-UTF-8 content.

### 5.3 Validation summary + row-issue shape (maps to design states #14)
```json
{
  "validation": {
    "status": "ok | ok_with_warnings | blocked",
    "rows_total": 10, "rows_valid": 9, "rows_invalid": 1,
    "columns_expected": ["record_id","customer_id","customer_name","date","day_index","peak_units","offpeak_units"],
    "columns_detected": ["record_id","customer_id","customer_name","date","day_index","peak_units","offpeak_units"],
    "columns_missing": [],
    "issues": [
      { "row_number": 11, "record_id": 10, "customer_id": "C11",
        "field": "peak_units", "code": "NEGATIVE_UNITS",
        "message": "peak_units is negative (-5.0); the row was excluded." }
    ],
    "issues_truncated": false
  }
}
```
The design's **"Row issue (issue label + description)"** `[obs]` maps to `code` + `message`;
**"Validated dataset summary (… + status dot/label)"** `[obs]` maps to `rows_*` + `status`.

### 5.4 Issue-code catalogue (row level → HTTP 201 with `ok_with_warnings`)
`MISSING_VALUE`, `NEGATIVE_UNITS`, `UNPARSEABLE_NUMBER`, `UNPARSEABLE_DATE`,
`INVALID_DAY_INDEX`, `DUPLICATE_RECORD_ID`, `UNEXPECTED_EXTRA_COLUMNS`.

### 5.5 File-level codes (→ 4xx, no dataset)
`EMPTY_FILE` (400), `MISSING_COLUMNS` (422), `DUPLICATE_HEADER` (422), `NOT_CSV`/`UNSUPPORTED_MEDIA_TYPE` (415),
`UNSUPPORTED_ENCODING` (400), `FILE_TOO_LARGE` (413), `TOO_MANY_ROWS` (413), `NO_VALID_ROWS` (422 on analyse).

### 5.6 Caps (proposed defaults — Q14)
Max file size **5 MiB**, max rows **50 000**, max columns **32**, max cell length **256**, issues
returned **≤ 200** (then `issues_truncated: true`). Encoding: UTF-8 (BOM tolerated). Delimiter: `,`.

---

## 6. Authentication and authorization

### 6.1 Who does what
- **Supabase Auth** handles **email + password** (with e-mail verification and password reset),
  **Google**, and **GitHub** OAuth. It issues short-lived **JWT access tokens** + refresh tokens.
- **FastAPI** never handles passwords. It **verifies** the access token and enforces ownership.
- The browser talks to Supabase Auth directly (SDK) and to FastAPI with the bearer token.

### 6.2 Token verification (FastAPI)
1. Read `Authorization: Bearer <token>`; missing/blank → `401 UNAUTHENTICATED`.
2. Verify the signature against the project **JWKS** (asymmetric `RS256`/`ES256`; keys cached, refreshed
   on `kid` miss). *Do not* trust an unverified `alg`.
3. Validate `iss` (project URL), `aud` (`authenticated`), `exp`/`nbf` (small clock skew), and `sub`.
4. Look up/ensure the `profiles` row; attach `user_id = sub` to the request context.
5. Any failure → `401 UNAUTHENTICATED` (no detail leak).
> D-4 is still open (cookie/BFF vs bearer). This spec assumes **bearer** in the API and lets the UI
> hold the session; if you choose a BFF cookie model, FastAPI is called server-side with the token.

### 6.3 Authorization / ownership
- Every query is filtered by `user_id = auth.uid()`; the API additionally checks object ownership and
  returns **404** (not 403) for another user's id, to avoid existence leaks `[inf]`.
- **Defence in depth:** RLS is the database backstop; the API check is the primary gate.
- Service-role key is **server-side only**, never shipped to the browser; it bypasses RLS and is used
  only for privileged jobs (e.g. sample instantiation, retention).

### 6.4 Auth behaviours the design implies
| Design state `[obs]` | Required backend behaviour |
|---|---|
| Sign up → **Email verification sent** + **Resend verification email** | `signUp` sends a confirmation mail; resend endpoint/cooldown; unverified sign-in returns a specific error |
| **Incorrect credentials** + **Try again** / recovery link | `invalid_credentials` mapped to a safe message; password reset flow |
| **Required field validation** | Server-side `422` mirroring the client rules; messages returned per field |
| **Sign up · Password validation** | Password policy (length/character rules — Q9) + confirm match |
| Google / GitHub buttons | OAuth providers enabled in Supabase; callback to the app |
| Account → **Initials** | `profiles.display_name` / derived initials |

---

## 7. Questions and assumptions needing your review

### Questions
- **Q1 — Figma access.** **Resolved for inspection:** MCP connected; all 15 frames screenshot-read.
  Remaining `[unknown]`: prototype links, hover, keyboard. D-8 (accept this UI?) is still yours.
- **Q2 — The two bill lines.** Figma `[figma-obs]` is **(a)** peak × $0.30 and off-peak × $0.20
  with a single USD total. Product `[code]` must still expose **TOU and slab separately** in Rs
  (INV-11). Confirm the **implemented** report: Figma household mock vs PRD multi-customer
  analyzer (FSM, ranking, both bills).
- **Q3 — Expected-columns guide shows 5 columns, schema has 7**, and Figma’s fifth header is
  `off_peak_units` not `offpeak_units`. Which headers does upload actually require?
- **Q4 — "Editable usage chart"** is only a **layer name** `[figma-obs]`; no edit UI. Confirm
  read-only (PRD) vs editable recompute (not in PRD).
- **Q5 — Navigation labels.** **Observed:** Dashboard, Datasets, Reports, Settings. No Datasets
  list, Reports list, or Settings frame exists. Build those, drop the items, or add frames?
- **Q6 — One report per dataset-run?** Confirm ADR-014 (immutable snapshot; re-run = new row).
- **Q7 — Sample datasets.** Figma is one **Rowan House** 30-day file. Product has three bundled
  CSVs. Which samples does “Try sample data” expose?
- **Q8 — Sync vs async upload/analysis.** In-progress **64%** + Cancel `[figma-obs]` suggest
  async or a client progress bar. Choose one.
- **Q9 — Password policy.** Figma: **at least 8 characters** only. Confirm length/complexity.
- **Q10 — Duplicate uploads.** Reject a byte-identical re-upload, or create a new dataset?
- **Q11 — Report naming.** Figma uses month titles (“September 2026”). Auto vs user-supplied?
- **Q12 — Chart data source.** Figma buckets **5-day** bars for 30 days. Engine datasets are
  typically **3 days**. Series table vs `result_json`?
- **Q13 — Design tokens / copy.** **Resolved as observations** in `DESIGN.md` §8.2 (hex, Inter,
  spacing). Still **not accepted** until D-8.
- **Q14 — Limits.** Figma: **10 MB** CSV. This spec proposed **5 MiB** / 50 000 rows. Confirm.
- **Q15 — Anomaly flag.** Budget uses `circle-check` + “Within your budget”; no separate
  anomaly metric `[figma-obs]`. Decorative unless you want one.
- **Q16 — Currency.** Figma `$` vs analyzer `Rs`. **Keep analyzer Rs**; do not retarget goldens.
- **Q17 — Invalid rows.** Figma: “No report has been created” for two bad rows. INV-10: analyse
  valid rows. Which UX?
- **Q18 — Household vs fleet.** Figma shows one customer (Alex Morgan / C001). PRD FR-C3 requires
  ranked customers with FSM/trend. How should the real report look?

### Assumptions (flagged, reversible)
- **A1** The web app must reproduce golden results **exactly** (TC1 223 units/TOU Rs 780; TC2 291/TOU
  Rs 1040, C07 **slab** over budget; TC3 10→9→1 invalid, 191/TOU Rs 660) — from `Brain/PRD.md` §7
  and the analyzer (not from Figma).
- **A2** "Report" = one analysis run of one dataset, stored as an immutable snapshot (ADR-014) —
  **proposed**, not accepted.
- **A3** TOU and slab are always returned **separately**; nothing in the UI merges them silently (INV-11).
- **A4** Engine extraction into `analyzer_core` is **ADR-013 proposed**. Do not rewrite formulas.
  Baseline test results belong in `Brain/TEST_PLAN.md` (run them; do not copy stale “OK” claims).
- **A5** The uploaded CSV is the only analysis input; sample datasets are copies of the three bundled
  files.
- **A6** The design's 6-bar / 5-day chart and 420 kWh / $109.20 figures are **sample mocks**
  `[figma-obs]`; real reports use analyzer output (goldens; datasets often have 3 days).
  **Never** feed Figma numbers into the engine.
- **A7** RLS is enabled on every table; the API is the primary authorization gate and returns 404 for
  non-owned ids.
- **A8** Any inference marked `[inf]` is provisional until you confirm it in this section.

### Invariants restated (do-not-break checklist)
INV-1 bands `<10/10–19/20–29/≥30` · INV-2 states `LOW/MODERATE/HIGH/OVERLOAD` · INV-3 next state =
band's state · INV-4 high-usage `≥20` · INV-5 TOU `peak×4+offpeak×2` · INV-6 slab `3x` else
`150+5(x−50)` · INV-7 budget `Rs 500` → 120 units · INV-8 least-squares trend + day `n+1` prediction ·
INV-9 CSV header · INV-10 invalid = missing/negative, excluded · INV-11 **TOU ≠ slab, kept separate**.

---

### Review gate
**Do not implement this spec as-is.** Analyzer math is locked; Figma UI is observed but not
accepted (D-8). Next useful engineering step after Phase 0 is **Stage 1** in `Brain/TASKS.md`
(extract `analyzer_core` with no behavior change), after ADR-010–012. Q1/Q13 (MCP + tokens)
are answered as observations; Q2–Q12, Q14–Q18 and D-8 remain owner decisions. Code already
answers INV-9 = **7 CSV columns** and INV-11 = keep TOU and slab distinct.
