# BACKEND_SPEC — Electricity Consumption Analyzer (Web)

Status: **Draft / assumptions-heavy** · Last updated: 2026-10-18  
**Phase 0 audit:** this file is **not** an approved product spec. Visual design is **undecided**
(`Brain/DESIGN.md`, D-8). Do not implement from Figma-derived screens, copy, or tokens until
the owner selects a direction.

Precedence (must win over this draft):
1. Cursor chat instructions
2. Behavior in `server.py` / `client.py` / `tests.py` / datasets
3. `Brain/DECISIONS.md` and `Brain/PRD.md`
4. Other Brain docs
5. **This file** — API/schema ideas may be reused later; Figma inventory is `[figma-draft]`

What **is** evidence-backed here: INV checklist and analysis JSON contract (`[code]`), matching
`Brain/PRD.md`. What is **not**: approved UI, 5-column upload guide vs 7-column CSV, editable
chart, nav labels, async upload jobs, password policy, file caps, “estimated total” mapping.

Sources of truth used:
- **Calculations/behaviour:** `server.py`, `client.py`, `tests.py`, `testcases.py`, `README.md`,
  `dataset.csv`, `dataset_high.csv`, `dataset_edge.csv` (unchanged — see §0.3).
- **Phase 0 docs:** `Brain/PRD.md`, `Brain/ARCHITECTURE.md`, `Brain/DESIGN.md`, `Brain/DECISIONS.md`,
  `Brain/RULES.md`, `Brain/SECURITY.md`, `Brain/TEST_PLAN.md`, `Brain/TASKS.md`, `Brain/MEMORY.md`.
- **Design (UNAPPROVED draft):** a Figma file was used in an earlier session
  (`figma.com/design/QpIaPoDpZVCS2jno7Gn6Nk/Untitled`, 15 frames). Treat frames as
  `[figma-draft]`, not as locked UX.

> **Legend used throughout:** `[obs]` = directly observed in the Figma file ·
> `[inf]` = necessary inference (needs your confirmation) · `[code]` = taken verbatim from the
> existing analyzer code.

---

## 0. How this spec was derived

### 0.1 Figma access — important disclosure
You asked me to use the design **through the connected Figma MCP server**. I verified that
**no Figma MCP server is connected** and could not use one:

- The tool catalog contains **no Figma/MCP tools** (`search` for `figma`, `mcp`, `get_design`,
  `code_connect` returns only the generic `opencode.list_mcp_resources` / `read_mcp_resource`).
- `list_mcp_resources({})` returns **empty** `resources` and `templates`.
- `list_mcp_resources({server:"figma"})` → **`MCP server not found: figma`**.

I did **not** guess. Instead I read the **same Figma file** through the browser tab already open
in this session (valid share token), the same way as earlier. That gives me the **complete layer
tree** (all 15 frames, expanded recursively: 1 385 rows) — i.e. every screen, region, component
and state present in the file.

**What the browser route cannot give me:** the literal copy strings, hex colours, font sizes and
spacings. Those live on the canvas and are not exposed as DOM text. Where the design's *intent*
depends on such a value I have marked it `[inf]` and raised a question in §7 rather than inventing
it. If you want the exact tokens/copy, please connect the Figma MCP server (or paste Dev Mode
values) and I will fold them in.

### 0.2 Scope discipline
Sections 1–2 inventory a **Figma draft**. They are **not** Phase 0 requirements. Product
behavior is INV-1…INV-11 in `Brain/PRD.md`. `[inf]` and `[obs]` items stay open until the
owner picks a visual direction (D-8) and answers §7.

### 0.3 Existing analyzer is unchanged
No file outside `docs/` was created or modified in this phase. The analyzer, tests and datasets are
untouched; calculations below are quoted from the current code and are the authority.

---

## 1. Figma screen inventory and the user actions each supports

The file contains **15 frames** `[obs]`, grouped into four families:

| # | Frame `[obs]` | Family | Purpose |
|---|---|---|---|
| 1 | **Sign in · Desktop** | Auth | Email/password + Google/GitHub sign-in (desktop) |
| 2 | **Sign in · Mobile** | Auth | Same, mobile layout |
| 3 | **Sign up · Desktop** | Auth | Account creation (desktop) |
| 4 | **Sign up · Mobile** | Auth | Same, mobile layout |
| 5 | **Dashboard · Desktop** | App | Home: latest dataset, monthly summary, recent reports |
| 6 | **Dashboard · Mobile** | App | Same, mobile layout |
| 7 | **Upload dataset · Desktop** | App | Choose/upload a CSV; column guide; sample data |
| 8 | **Upload dataset · Mobile** | App | Same, mobile layout |
| 9 | **Analysis results · Desktop** | App | The report |
| 10 | **Analysis results · Mobile** | App | Same, mobile layout |
| 11 | **Dashboard · Desktop · New account** | Empty state | First-run dashboard (no datasets) |
| 12 | **Dashboard · Mobile · New account** | Empty state | Same, mobile layout |
| 13 | **Account feedback · Validation and verification** | Feedback | Auth form/error/verification states |
| 14 | **Upload feedback · Progress, success and errors** | Feedback | Upload progress/success/error states |
| 15 | **Current · Foundations and patterns** | System | Palette, typography/spacing, field & feedback patterns |

### 1.1 Sign in · Desktop `[obs]`
Two regions: a marketing **Welcome panel** and the **Account area**.

- Welcome panel: brand mark + brand name; "Energy introduction" (promise heading + description,
  an illustrative energy card with example usage + unit, an illustrative trend of six usage bars,
  a status chip); a "Reassurance" line with a shield-check icon + description.
- Account area: **Utility links → Help**; a sign-in form:
  - Page heading (title + description).
  - **Email field** (label + input + value).
  - **Password field** (label + input + value + visibility toggle `eye-off`).
  - A password-recovery action (forgot-password) `[inf: item present, exact copy not readable]`.
  - **Sign in** action (primary button).
  - **Alternative divider** (divider + label + divider).
  - **Social account options:** "Continue with Google" (Google mark + label), "Continue with GitHub" (github icon + label).
  - **Create account prompt** (link to sign-up).
  - **Legal links** (Privacy · Terms).
- **Actions:** enter email; enter password; toggle password visibility; submit sign-in; recover
  password; continue with Google; continue with GitHub; go to create account; open Help; open
  Privacy/Terms.

### 1.2 Sign in · Mobile `[obs]`
Same **Account area** as desktop; the Welcome panel is dropped and a compact "Mobile brand"
header is used instead. Same actions.

### 1.3 Sign up · Desktop `[obs]`
Welcome panel (as above) + Account area:
- Page heading (title + description).
- **Social account options:** "Sign up with Google", "Sign up with GitHub".
- **Alternative divider**.
- **Registration fields:** **Name field**, **Email field**, **Password field** (+ a `Hint`
  sub-label), **Confirm password field**; a description; **Create account** action.
- **Sign in prompt** (link to sign-in); **Legal links** (Privacy · Terms).
- **Actions:** sign up with Google/GitHub; enter name/email/password/confirm; toggle visibility;
  submit create-account; go to sign-in; open Help/Privacy/Terms.

### 1.4 Sign up · Mobile `[obs]`
Same Account area + Mobile brand; same actions.

### 1.5 Dashboard · Desktop `[obs]`
- **App header:** brand (mark + name + product descriptor); **Main navigation** with **4 items**:
  icons `layout-dashboard`, `files`, `chart-no-axes-column`, `settings`
  `[inf: labels ≈ Dashboard / Datasets / Reports / Settings — labels are unreadable text nodes]`;
  **Account → Initials** (avatar).
- **Page content:**
  - **Welcome and action:** page heading (title + description) + an **"Upload a dataset"** action (upload icon).
  - **Latest dataset context:** a period + a status chip (status dot + label).
  - **Monthly summary:** **3 summary cards**, each `label+icon → value → supporting detail`;
    icons `zap`, `wallet`, `circle-check`.
  - **Recent reports:** section heading with a **report count**; a table with column labels
    (name · date · figures · action); **3 recent report rows**, each = report symbol
    (`file-chart-column`) + report title + report date + created date + report figures
    (**Usage**, **Estimated bill**) + a **"View report"** action (`arrow-up-right`); plus a description.
  - **Page footer:** footer note + Help link.
- **Actions:** navigate to the four primary destinations; start upload; open a recent report;
  view latest dataset period/status; read monthly summary.

### 1.6 Dashboard · Mobile `[obs]`
Same content without the table's column headings, plus a bottom **Main navigation** bar. Same actions.

### 1.7 Upload dataset · Desktop `[obs]`
- App header (+ a **Back link**).
- Page heading (title + description).
- **Upload steps:** 3 steps, each = step marker (step number) + step label.
- **CSV drop area:** upload symbol (`cloud-upload`); drop instructions (drop heading + description);
  **"Browse files"** (`folder-open`); a file-limits note.
- **File preparation → Expected columns** table: guide heading (title + description); table headings
  (**column · example · help**); and **exactly 5 column definitions**, each = column name
  (field label + **CSV header**) + example value + format hint. See §5.1 for the 5-versus-7 mismatch.
- **Sample dataset help:** `file-spreadsheet` icon; sample explanation (title + description);
  **"Try sample data"**; a **download** link for the sample; a description.
- **Privacy note** (`shield-check` + description).
- Page footer.
- **Actions:** go back; drag-and-drop a CSV; browse files; read the column guide; try sample data;
  download the sample; read the privacy note.

### 1.8 Upload dataset · Mobile `[obs]`
Same, with a "Back to dashboard" link and a bottom Main navigation bar; the expected-columns guide
shows `Date format` on one column. Same actions.

### 1.9 Analysis results · Desktop `[obs]`  ← the report
- App header (+ nav + account avatar).
- **Report breadcrumb:** back arrow + back link + separator + current report.
- **Report header:** page heading (title + description) + **status** (status dot + label).
- **Plain-language summary:** summary title + description.
- **Key figures:** **3 summary cards** (icons `zap`, `wallet`, `calendar-days`), each
  `label+icon → value → supporting detail`.
- **Consumption trend:** chart heading (title + legend {swatch + label}); usage-axis title;
  an **"Editable usage chart"** containing axis ticks+gridlines, **usage bars** (the design uses the
  same component 6×, labelled "Five-day usage"), and date ticks (**6 date labels**); a
  consumption date-axis title; a chart caption.
- **Bill and budget:**
  - **Estimated bill details:** bill heading (title + description); **2 bill lines**, each =
    charge description (**charge label** + **calculation**) + **amount**; an **estimated total**
    (total label + total); a description.
  - **Monthly budget:** budget heading (title + `circle-check`); **budget remaining**
    (amount + description); a **budget meter** (**used**); a description.
- Page footer.
- **Actions:** go back to the report list; read key figures; read the trend chart; read bill lines;
  read budget status.

### 1.10 Analysis results · Mobile `[obs]`
Same content + bottom Main navigation. Same actions.

### 1.11 Dashboard · Desktop · New account `[obs]` (empty state)
- **Welcome and action:** page heading.
- **No datasets:** a first-dataset illustration (`file-chart-column`) + an empty-state explanation
  (heading + description) + **first actions (Upload a dataset, Try sample data)** + a supported-file
  note (`info` icon).
- **What to expect:** section heading + getting-started steps (`circle-check` + description) —
  **1 step on desktop, 3 steps on mobile** (content is a design-mock detail).
- **Actions:** upload a dataset; try sample data.

### 1.12 Dashboard · Mobile · New account `[obs]`
Same, with 3 getting-started steps + bottom Main navigation.

### 1.13 Account feedback · Validation and verification `[obs]` — auth states
Four labelled states of the auth forms:

| State `[obs]` | Contents `[obs]` | Backend meaning `[inf]` |
|---|---|---|
| **Sign in · Required field validation** | email field with `circle-alert` + validation message; password field + validation message; Sign in | Client/server required-field validation failed |
| **Sign in · Incorrect credentials** | error message (icon + title + description); recovery actions (recovery link + "Try again") | Auth rejected the credentials |
| **Sign up · Password validation** | password field + validation message; confirm-password field + validation message; Create account + description | Password policy / mismatch failure |
| **Sign up · Email verification sent** | `mail-check` symbol; verification instructions (heading + 2 descriptions); **Back to sign in**; **Resend verification email**; description | Sign-up succeeded, e-mail not yet confirmed |

- **Actions:** retry sign-in; use recovery link; resend verification email; go back to sign-in.

### 1.14 Upload feedback · Progress, success and errors `[obs]` — upload states

| State `[obs]` | Contents `[obs]` | Backend meaning `[inf]` |
|---|---|---|
| **Upload · In progress** | selected CSV (file name + file size); upload progress (progress description + percentage, progress track + fill); **Cancel upload** | Upload/validation job running |
| **Upload · Success** | `circle-check`; success heading (title + description); selected CSV; **validated dataset summary** (row/column descriptions + status {dot + label}); **View analysis** | File accepted and parsed |
| **Upload · CSV validation error** | heading; selected CSV; error message (icon + title + description); **validation issues** = row issues (issue label + description); **Choose corrected file** | File rejected, or accepted with row-level issues |

- **Actions:** cancel upload; view analysis; choose a corrected file.

### 1.15 Current · Foundations and patterns `[obs]` — design system
- Sheet heading (brand + descriptor) and page heading.
- **Palette:** **6 colour references**, each = swatch + role + **hex value**
  `[inf: role names and hex values are text, not readable via the browser route]`.
- **Typography and spacing:** a typography reference (font family) + 4 type samples; a layout
  reference with **7 spacing references** + radius references (control radius, card radius) +
  responsive rules.
- **Fields and feedback:** form patterns (field default + error states; primary/secondary/unavailable
  button treatments); status patterns (two status labels + a success message + an error message).

> This frame defines the **presentation** system. It is referenced here only because it confirms the
> feedback vocabulary (status labels, success/error messages, button "unavailable" state) the API must
> be able to drive. Exact tokens remain design-owned (§7, Q13).

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
| Bill line 1 / line 2 (`charge label` + `calculation` + `amount`) | **open** — see Q2: either TOU components (peak/off-peak) or TOU vs slab | `GET /api/v1/reports/{id}` |
| Estimated total | `summary.total_tou_bill` (or TOU+slab — Q2) | `GET /api/v1/reports/{id}` |
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

> ⚠️ **Mismatch to resolve (Q3):** the design's "Expected columns" guide shows **exactly 5 columns**
> `[obs]` (desktop and mobile), each with a *CSV header*, example and format hint — while the CSV
> schema (INV-9) has **7 fields**. Likely the guide lists only the 5 user-meaningful columns
> (customer id, customer name, date, peak units, off-peak units) and omits `record_id` / `day_index`.
> **The backend will still require all 7 (INV-9) unless you decide otherwise.**

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
- **Q1 — Figma access.** No Figma MCP server is connected; I read the file via the browser tab
  (structure only — see §0.1). **Do you want to connect the Figma MCP server** so I can also extract
  exact copy, hex colours and spacing, or is the structural reading sufficient?
- **Q2 — The two bill lines.** "Estimated bill details" shows **2 bill lines** `[obs]`. Is that
  **(a)** TOU split into peak/off-peak, **(b)** TOU vs slab, or **(c)** something else? The backend will
  expose `tou_bill` and `slab_bill` **separately** regardless (INV-11); I just need to know what the two
  lines and the "Estimated total" represent.
- **Q3 — Expected-columns guide shows 5 columns, the schema has 7** (§5.1). Which columns will the UI
  actually require? (`record_id`/`day_index` may be auto-generated.)
- **Q4 — "Editable usage chart"** `[obs]`. Is the chart *editable* (does the user change values and the
  bill recompute)? If yes, that needs a recalculate endpoint — please confirm, since it is not in the PRD.
- **Q5 — Navigation labels.** The 4 nav items show only icons `[obs]`
  (`layout-dashboard`, `files`, `chart-no-axes-column`, `settings`). Confirm the labels
  (Dashboard / Datasets / Reports / Settings?).
- **Q6 — One report per dataset-run?** Confirm that "Run analysis" creates a **new immutable report**
  each time (ADR-014), and that "Re-run" always creates a new one.
- **Q7 — Sample datasets.** Should "Try sample data" expose the three bundled CSVs
  (`dataset.csv`, `dataset_high.csv`, `dataset_edge.csv`) as the samples? Any renames/descriptions?
- **Q8 — Sync vs async upload/analysis.** The "In progress / Cancel" states `[obs]` suggest async.
  Should `POST /datasets` be async (job id) or synchronous with a client-side progress bar?
- **Q9 — Password policy.** The "Sign up · Password validation" state `[obs]` — what exact rules
  (minimum length, complexity) should the API report?
- **Q10 — Duplicate uploads.** Reject a byte-identical re-upload, or create a new dataset?
- **Q11 — Report naming.** Auto-name (e.g. `"<dataset> · <date>"`) or let the user name it?
- **Q12 — Chart data source.** Serve the chart series from `report_series`, or render it from
  `result_json.daily_units`? (Affects §3.6.)
- **Q13 — Design tokens / copy.** Palette hex values, roles, typography and spacing in frame #15 are
  text I could not read. Do you want the Figma MCP route (Q1) to pull them, or will you provide them?
- **Q14 — Limits.** Confirm the §5.6 caps (5 MiB / 50 000 rows / 200 issues) and the export formats
  (CSV only, or PDF too — D-6).
- **Q15 — Anomaly flag.** The Analysis screen has a `chart-no-axes-column`-style icon next to the budget
  heading (`circle-check`) `[obs]`. Is any of these a distinct "warning/anomaly" flag I must compute, or
  purely decorative?

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
- **A6** The design's 6-bar / 5-day chart is a mock `[obs]`; the real chart must handle **any** number of
  days (the datasets have 3).
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
**Do not implement this spec as-is.** Analyzer math is locked; Figma UI is not. Next useful
engineering step after Phase 0 is **Stage 1** in `Brain/TASKS.md` (extract `analyzer_core` with
no behavior change), after the owner confirms ADR-010–012. Q1–Q15 remain open except where
code already answers them (INV-9 = **7 CSV columns**; INV-11 = keep TOU and slab distinct).
