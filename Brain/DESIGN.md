# DESIGN — UX & visual direction

Status: Draft · **D-8 still open** (Figma is observed, not accepted) · Last updated: 2026-10-18

This file records UX requirements that do not depend on look-and-feel, plus a
**Figma observation log** from MCP (file [Untitled](https://www.figma.com/design/QpIaPoDpZVCS2jno7Gn6Nk/Untitled?node-id=0-1),
page **Page 1**). Observed tokens, copy, and layouts stay **`[figma-obs]`** until
you accept D-8. They are **not** a locked aesthetic.

Legend: `[figma-obs]` = read from Figma MCP screenshot + generated structure ·
`[code]` = analyzer behavior · `[inf]` = inference · `[unknown]` = not exposed
(prototype links, hover, keyboard, loading beyond the static “in progress” card).

**Illustration numbers and currency in Figma are sample design content.** Do not
use `$20.80`, `$109.20`, `$130`, `$0.30/$0.20`, or `420 kWh` as report data.
The analyzer reports **Indian rupees (`Rs`)** and its own calculated values
(`[code]` INV-5…INV-7). Never change analyzer behavior to match the mock.

---

## 1. Visual direction — DECISION SLOTS (all open)

| # | Decision | Status | Notes |
|---|---|---|---|
| V-1 | Brand / tone | ⛔ undecided | utilitarian analyst vs consumer-friendly vs enterprise |
| V-2 | Color system | ⛔ undecided | needs semantic colors for FSM states that are not color-only |
| V-3 | Typography | ⛔ undecided | |
| V-4 | Layout density | ⛔ undecided | |
| V-5 | Component library | ⛔ undecided | |
| V-6 | Data visualization | ⛔ undecided | charts vs tables (also D-7) |
| V-7 | Iconography | ⛔ undecided | |
| V-8 | Motion | ⛔ undecided | must respect `prefers-reduced-motion` |

**Non-aesthetic constraint:** `LOW` / `MODERATE` / `HIGH` / `OVERLOAD` and
over-budget vs in-budget must be distinguishable by **text (and preferably
shape/icon)**, not color alone.

---

## 2. UX principles (direction-agnostic)

- P-1 **Trust:** reports show inputs, timestamp, and engine version.
- P-2 **Guardrails:** validate CSV shape before/with the run; show which rows
  were invalid and why.
- P-3 **Revisit is a snapshot:** opening a saved report does not silently recompute.
- P-4 **Progressive disclosure:** totals first; per-customer FSM/trend on demand.
- P-5 **No dead ends:** every error names the problem and the next action.
- P-6 **Do not conflate bills:** TOU and slab always appear as distinct figures.

## 3. Core flows (behavioral)

### 3.1 First run
`Sign in (email/password | Google | GitHub) → Upload CSV or choose sample → Validate → Run → Report (auto-saved)`

### 3.2 Revisit
`Sign in → Reports list (newest first) → Open snapshot → optional explicit Re-run`

### 3.3 Upload validation
Show filename, detected columns, received/valid/invalid counts.  
**Block** if required headers (INV-9) are missing.  
**Allow** if some rows are invalid (INV-10): analysis still runs on valid rows.

## 4. Accessibility

- WCAG 2.1 AA target.
- Keyboard operable; visible focus.
- Charts (if any) have a text/table alternative.
- Errors associated with fields.
- No motion required to understand content.

## 5. Information architecture (sitemap proposal)

```
/                     marketing or redirect to sign-in
/sign-in  /sign-up  /reset  /verify  /oauth-callback
/app                  dashboard: recent reports, start a run
/app/datasets         list, upload, sample pick, preview, delete
/app/reports          list
/app/reports/:id      snapshot detail, export, re-run
/account              profile, linked providers, sessions
(optional) /s/:token  read-only share (D-6)
```

Figma chrome `[figma-obs]` (not accepted): brand **current** / “Electricity analyzer”;
in-app nav **Dashboard · Datasets · Reports · Settings**; desktop header, mobile
bottom bar. No Settings / Datasets-list / Reports-list frames exist. Prototype
destinations `[unknown]`.

## 6. Report content (must be representable, regardless of look)

From the existing printer (`client.print_report`) and `analyze_records`:

1. **Summary:** records received / analyzed / invalid; customer count; total
   units; **total TOU bill**; average units per record.
2. **Per customer (ranked by total units):** id, name, total units, TOU bill,
   slab bill, daily units, FSM path, final state, recommendation, trend
   equation, next-day prediction.
3. **High-usage records:** `total_units >= 20`, with date and TOU bill.
4. **Budget:** monthly Rs 500, max units allowed (120 for that budget),
   customers over budget (slab vs Rs 500).

Copy today uses `Rs` and the recommendation strings in `RECOMMENDATIONS`.

## 7. Open design questions

1. Phase 1 charts or tables only (D-7)? Figma shows a 6-bar “Electricity use”
   chart (5-day buckets). Still not accepted.
2. Multi-report comparison in Phase 1 or later?
3. Light / dark / both? Figma is light-only `[figma-obs]`.
4. How prominent is engine version / reproducibility? Figma report footer shows
   filename / reading count / created date, not `engine_version`.
5. Printable report view (legacy assignment hard-copy is not a product requirement)?
6. How to present **two** bills (TOU vs slab) so they cannot be mistaken for one
   total? Figma shows **one** “Estimated bill” split peak/off-peak in **USD**,
   not TOU vs slab in Rs.
7. Accept, adapt, or reject the Figma “Current” visual system (D-8)?
8. Currency and sample rates: keep analyzer `Rs` + INV-5/6, or change by ADR?
9. CSV guide shows **five** columns including `off_peak_units`; INV-9 is **seven**
   columns with `offpeak_units` (no underscore).
10. Invalid-row UX: Figma blocks the report (“No report has been created”);
    INV-10 still analyses valid rows.

---

## 8. Figma observations (MCP, not accepted)

Source: Figma MCP `get_metadata` + `get_design_context` (screenshot + layer
structure) on 2026-10-18. Session file key `QpIaPoDpZVCS2jno7Gn6Nk`. Prototype
interactions `[unknown]` (`get_motion_context` was not completed). Named Figma
variables on the foundations frame returned `{}`.

### 8.1 Screen / state inventory `[figma-obs]`

All 15 top-level frames were **visually inspected** (screenshot viewed), not
metadata-only.

| Frame | Node | Size | Role / visible state |
|---|---|---|---|
| Sign in · Desktop | `2:11990` | 1280×900 | Split welcome + form |
| Sign in · Mobile | `2:12058` | 390×844 | Form only; no welcome panel |
| Sign up · Desktop | `2:12099` | 1280×1013 | Split welcome + registration |
| Sign up · Mobile | `2:12176` | 390×997 | Form only |
| Dashboard · Desktop | `2:12226` | 1280×967 | Populated home |
| Dashboard · Mobile | `2:12335` | 390×1475 | Same content, stacked + bottom nav |
| Upload dataset · Desktop | `2:12425` | 1280×1284 | Step 1 Upload highlighted |
| Upload dataset · Mobile | `2:12541` | 390×1662 | Browse-first; drag mentioned as extra |
| Analysis results · Desktop | `2:12648` | 1280×1537 | Household-style report mock |
| Analysis results · Mobile | `2:12779` | 390×2027 | Same; Daily-average card omitted (folded into usage caption) |
| Dashboard · Desktop · New account | `2:12899` | 1280×920 | Empty datasets |
| Dashboard · Mobile · New account | `2:12950` | 390×1002 | Empty datasets; 3 stacked steps |
| Account feedback · Validation and verification | `2:13005` | 1280×848 | Four auth states on one sheet |
| Upload feedback · Progress, success and errors | `2:13072` | 1280×672 | Three upload states on one sheet |
| Current · Foundations and patterns | `2:13139` | 1280×1226 | Tokens and control patterns |

**No dedicated screens** `[figma-obs]`: Settings, Datasets list, Reports list
(only “Recent reports” on dashboard and a breadcrumb “Reports”), password-reset
form, OAuth callback, logout, per-customer ranking, FSM path, high-usage list,
slab vs TOU table.

### 8.2 Tokens `[figma-obs]` (Foundations frame)

| Role | Hex |
|---|---|
| Action | `#2864D7` |
| Positive | `#247653` |
| Text | `#172B43` |
| Secondary | `#607087` |
| Canvas | `#F7F9FC` |
| Border | `#DFE6EF` |

Also used on screens (not named on the palette): error `#B53C3C`, error wash
`#FFF0EF`, success wash `#EAF6EF`, selected-nav / drop wash `#EBF2FF`, welcome
panel `#F0F5FC`, bar fill `#C6D8FA`, focus ring Action 2 px.

- **Type:** Inter. Page title 32/38 Semibold (mobile 27/32). Section 20/28
  Semibold. Body 16/24 Regular. Supporting 13/20 Regular. Brand wordmark 22 Bold.
- **Space:** 4, 8, 12, 16, 24, 32, 48. Groups 24–32; within-group 8–16.
  Controls ≥ 46 px tall; inputs 48 × 10 px radius; cards 16 px radius.
- **Responsive copy on the sheet:** Desktop 1280, 88 px page margins. Mobile
  390, 20 px margins. Stack cards/report rows; move navigation below content.
- **Fields:** visible labels; focused field 2 px Action border; error 1 px
  `#B53C3C` + written explanation. Buttons: Primary (Action), Secondary (white +
  border), Unavailable (`#DFE6EF` + secondary text).
- **Status:** pill “Ready” (green) and “Latest report” (blue-grey); success and
  error banners always include title + body text (not color alone) — matches P-2
  / accessibility note in §4.

### 8.3 Auth screens `[figma-obs]`

**Desktop sign-in / sign-up:** 500 px left welcome (`#F0F5FC`): brand, “Less
guessing. / More clarity.”, illustrative card **420 kWh in September**, six
usage bars, chip **“$20.80 under budget”** (sample), “Your data stays in your
account.” Form column 400 px; “Need help?” top-right.

**Mobile:** welcome panel dropped; compact brand; page title 27 px; horizontal
padding 24 px.

Sign-in copy: “Welcome back” / “Sign in to understand your energy use.” Email
placeholder `you@example.com`. Password + eye-off. “Forgot password?” Sign in.
“or continue with” Google / GitHub. “New to Current? Create an account.” Privacy ·
Terms.

Sign-up copy: “Make sense of your energy” / “Create your free Current account.”
Google/GitHub **first**, then “or use your email.” Fields: Name, Email, Password
(hint **“Use at least 8 characters.”**), Confirm password. Verification note.
Create account. “Already have an account? Sign in.”

**Account feedback states** (static cards, not routed screens):

- Sign in / Field validation — “Check your details”; incomplete email `alex@`;
  empty password.
- Sign in / Account error — “The email or password isn’t right.” + Forgot
  password? + Try again.
- Sign up / Field validation — “Almost there”; password &lt; 8 chars; mismatch;
  “Your other details are kept.”
- Sign up / Verification sent — “Check your inbox” to `alex@example.com`; Back
  to sign in; Resend verification email.

### 8.4 App chrome and dashboard `[figma-obs]`

Header 88 px (desktop) / 76 px (mobile). Nav labels **Dashboard, Datasets,
Reports, Settings**. Active item Action text on `#EBF2FF`. Avatar initials
**AM**. Footer “A little clarity for your energy.” Desktop also “Need help?”

**Populated dashboard:** “Hello, Alex” / “Your latest month, at a glance.”
Primary “Upload a dataset”. Context “Rowan House · 1–30 September 2026” +
“Latest report”. Cards: Total usage **420 kWh** (252 peak · 168 off-peak);
Estimated bill **$109.20** (“Illustrative rates, not a utility bill”); Budget
status **On track** (“$20.80 left of your $130 budget”). Recent reports (3):
Sep/Aug/Jul 2026 with kWh and `$` estimates. Rate footnote:
`$0.30/kWh` peak and `$0.20/kWh` off-peak.

**Mobile:** upload button full width under heading; summary cards stacked;
report rows compact + full-width “View report”; no table column headers; no
footer Help link.

**New account:** “Welcome, Alex” / “Let’s make sense of your electricity use.”
Empty card “Your energy story starts here”; Upload a dataset; Try sample data;
“CSV files up to 10 MB”. Desktop one-line steps; mobile three rows.

### 8.5 Upload `[figma-obs]`

Steps: **1 Upload** (active) · 2 Check file · 3 View report. Drop zone dashed
Action border. Desktop: “Drag and drop your CSV here”. Mobile: “Choose your CSV
file” + “You can also drag and drop”. Browse files. “CSV only · Up to 10 MB”.

Column guide title: “Use these **five** column names in the first row”:
`customer_id`, `customer_name`, `date`, `peak_units`, **`off_peak_units`**.
Examples C001 / Alex Morgan / 2026-09-01 / 8.4 / 5.6. Rule: one row per
customer per day; units ≥ 0; no blank cells.

Sample card: “Try Rowan House: 30 days… September 2026.” Try sample data ·
Download sample CSV. Privacy: “Your file is only used to create reports in your
account.”

**Upload feedback states:**

- In progress — `rowan-house-sep-2026.csv` 4.2 KB; **64%**; Cancel upload.
- Success — “Your file is ready” / “All 30 readings passed our checks.” /
  420 kWh / “No missing or invalid readings” / **View analysis**.
- Validation error — “Let’s fix two readings”; **“No report has been created.”**
  Row 12 date missing; Row 19 peak −4; **Choose corrected file**.

### 8.6 Analysis results `[figma-obs]`

Household mock, **one customer** Alex Morgan (C001), 30 days, 420 kWh.
Breadcrumb Reports / September 2026. Status “Report ready”. Summary uses `$`
and **$130 budget**. Key figures: usage, estimated bill, daily average 14 kWh
(desktop only as a third card). Chart layer named **“Editable usage chart”** —
six 5-day bars, no visible edit controls. Bill lines are **peak × $0.30** and
**off-peak × $0.20**, total `$109.20`. Budget remaining `$20.80 left` / 84%
used. Source line: `rowan-house-sep-2026.csv`.

**Not shown:** TOU vs slab, FSM path, recommendations, trend equation, next-day
prediction, high-usage list, invalid-row count, ranked customers, `engine_version`.

### 8.7 Desktop vs mobile `[figma-obs]`

| Pattern | Desktop | Mobile |
|---|---|---|
| Auth marketing panel | 500 px left column | omitted |
| Page title | 32 px | 27 px |
| App nav | header, 14 px labels | bottom bar, 10 px labels |
| Page padding | 88 px | 20 px |
| Summary cards | 3-up row | stacked; analysis drops the third card |
| Reports | table + inline View | stacked + full-width button |
| Upload primary | drag-and-drop | browse first |
| Empty-state steps | one combined line | three rows |
| Footer Help | yes | no |

### 8.8 Conflicts: Figma sample vs analyzer `[code]`

| Topic | Figma `[figma-obs]` | Analyzer `[code]` |
|---|---|---|
| Currency | `$` | `Rs` |
| TOU rates | $0.30 / $0.20 per kWh | peak×4 + offpeak×2 (INV-5) |
| Budget | $130; remaining vs estimated USD bill | Rs 500; over-budget = **slab** > 500 (INV-7); 120 units |
| Totals | 420 kWh, $109.20 | Goldens e.g. TC1 223 units, TOU Rs 780 |
| Customers | one (Alex Morgan / C001) | ranked multi-customer reports |
| CSV columns | 5; `off_peak_units` | 7; `offpeak_units` (INV-9) |
| Invalid rows | block report | exclude and continue (INV-10) |
| Sample data | fictional Rowan House 30-day file | `dataset.csv`, `dataset_high.csv`, `dataset_edge.csv` |
| Bills | one estimated total | TOU and slab **separate** (INV-11) |
| Units | kWh labels | `*_units` (unit name not in schema) |
| File cap | 10 MB | proposed 5 MiB in BACKEND_SPEC (Q14) |

**Do not** retarget goldens, rates, or budget to the illustration.

### 8.9 What remains `[unknown]` or missing in Figma

- Prototype click/hover/keyboard/focus beyond static focused/error fields.
- Destinations for Need help?, Privacy, Terms, Forgot password?, Settings, Datasets, Reports list.
- Loading besides the 64% upload card; OAuth redirect; logout; email-verified landing.
- Dark mode, reduced-motion, chart interactivity despite layer name “Editable”.
- How a **multi-customer** INV report maps onto this household UI.
