# DESIGN — UX & visual direction

Status: Draft · **Visual direction intentionally UNDECIDED** · Last updated: 2026-10-18

Per this phase: **do not choose a visual design yet.** This file records UX
requirements and open slots. Nothing here is a locked aesthetic, palette,
component library, or layout system.

A later Figma file, `docs/BACKEND_SPEC.md` screen inventory, or vibe-coding
example (including StudentHub-style samples) is **not** a specification for this
product. Those drafts stay `[figma-draft]` until D-8 is decided.

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

Labels and visual chrome are not designed yet.

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

1. Phase 1 charts or tables only (D-7)?
2. Multi-report comparison in Phase 1 or later?
3. Light / dark / both?
4. How prominent is engine version / reproducibility?
5. Printable report view (legacy assignment hard-copy is not a product requirement)?
6. How to present **two** bills (TOU vs slab) so they cannot be mistaken for one total?
