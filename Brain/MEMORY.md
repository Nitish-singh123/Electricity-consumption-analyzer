# MEMORY — Project state

Status: living · Last updated: 2026-10-18 (Phase 0 audit / reconcile)

Verified by inspection and by commands run this session. Nothing here is guessed.

---

## 1. Repository

| Item | Value |
|---|---|
| Requested folder | `E:\opencode_projects` (contains only `app_assignment`; **not** a git repo) |
| Git root / workspace | `E:\opencode_projects\app_assignment` |
| Branch | `master`, tracking `origin/master` |
| Remote | `https://github.com/Nitish-singh123/Electricity-consumption-analyzer.git` |
| Commits | `d99b259` first changes · `e1ea890` second changes |
| `.gitignore` | **none** (`__pycache__/*.pyc` is tracked) |
| App code dirty? | **No.** Tracked application files unchanged this phase. |

Untracked: `Brain/` (docs packet) and `docs/` (BACKEND_SPEC draft). Windows treats
`brain/` and `Brain/` as the same folder. `docs/BACKEND_SPEC.md` is **demoted**:
Figma screens/tokens are not approved (D-8); INV/`[code]` sections may be reused later.

## 2. As-is files

```
brain/                 this docs packet (9 markdown files)
client.py              TCP client, CSV loader, printer
server.py              TCP server + FSM + FP + SymPy
tests.py               17 unittests
testcases.py           live TC runner
dataset.csv            TC1 — 12 rows, 4 consumers × 3 days
dataset_high.csv       TC2 — 9 rows, 3 consumers
dataset_edge.csv       TC3 — 10 rows including C11 peak=-5
outputs/               committed printouts (title lines slightly older than live runner)
report/page1.md–4.md   handwritten assignment drafts (legacy)
*.bat                  Windows launchers
docs/                  untracked later draft (ignore for Stage 0)
```

CSV header (all three files):
`record_id,customer_id,customer_name,date,day_index,peak_units,offpeak_units`

## 3. Environment

- Windows, Python **3.12.10**, SymPy **1.14.0**.
- One pip dependency: `sympy`.

## 4. Commands that work

```powershell
cd E:\opencode_projects\app_assignment
python -m unittest -v
python testcases.py 1|2|3|all
python server.py                 # other terminal
python client.py --testcase 1
```

## 5. Baseline executed this session

`python -m unittest -v` (re-run) → **`Ran 17 tests in 0.316s` / `OK`**.

`python testcases.py all` → exit 0; goldens:

- TC1: 12/12/0, 223 units, TOU Rs 780, C03 rank 1 OVERLOAD, budget 120, none over.
- TC2: 9/9/0, 291 units, TOU Rs 1040, C07 slab Rs 600 over budget, 7 high-usage.
- TC3: 10/9/1, 191 units, TOU Rs 660, C10 10/20/30 boundaries, none over budget.

See `TEST_PLAN.md` for the full recorded figures.

## 6. Domain facts (do not change without ADR)

- Bands: `<10`, `10–19`, `20–29`, `≥30` → LOW / MODERATE / HIGH / OVERLOAD.
- Start state: LOW. Next state = band target (relapse allowed).
- High-usage: `total_units >= 20`.
- TOU: `peak×4 + offpeak×2`. Slab: `3x` (x≤50) else `150+5(x−50)`.
- Budget Rs 500 → **120 units** via slab solve. Over-budget = slab > 500.
- Trend: SymPy least squares; predict day n+1.
- Invalid: missing or negative peak/off-peak; excluded, counted.

## 7. Gotchas

- Over-budget is **slab**, while the summary total is **TOU**.
- Empty over-budget JSON is `["none"]`, not `[]`.
- Live `testcases.py` titles include `(dataset.csv)` etc.; committed `outputs/`
  titles do not. Numbers match.
- No packaging; run from the project directory (or use the `.bat` files).
- Port 65432: second server is refused by design.

## 8. Phase log

| Date | Phase | Outcome |
|---|---|---|
| 2026-10-18 | Stage 0 — inspect + `brain/` docs | 17 tests OK; TC1–3 live OK; 9 markdown files; **no app code changes** |
| 2026-10-18 | Stage 0 — audit/reconcile | Re-ran 17 tests (0.316s OK) + `testcases.py all`; labeled BACKEND_SPEC Figma items as unapproved; added `.cursor/rules`; **no app logic changes** |

## 9. Next (wait for instruction)

1. Review `Brain/` especially proposed stack ADR-010/011/012.
2. Call D-1…D-8 as needed (D-2, D-4, D-5, D-8 matter earliest).
3. Recommended next phase: **Stage 1** — extract `analyzer_core` (behavior-preserving) + `.gitignore` + `pyproject.toml`. Do not start UI/auth/DB until that lands and ADR-010–012 are confirmed.

Do **not** start implementation or pick a visual design until asked.

## 10. Glossary

- **FSM** — daily usage classifier (4 states).
- **TOU** — time-of-use bill (peak vs off-peak rates).
- **Slab** — 50-unit piecewise tariff used for `slab_bill` and budget.
- **Golden** — exact expected numeric/report result.
- **RLS** — row-level security.
- **BFF** — backend-for-frontend session holder (D-4 option).
