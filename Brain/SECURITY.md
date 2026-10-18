# SECURITY

Status: Draft · Last updated: 2026-10-18  
Requirements-level threat model for the **web** product. No security controls
were implemented in this phase.

---

## 1. Assets

| Asset | Why it matters |
|---|---|
| Credentials and OAuth sessions | Account takeover |
| Uploaded CSVs (names, usage) | Personal / behavioral data |
| Saved reports | Derived personal data |
| Analysis integrity | Wrong numbers destroy trust |
| Service-role / DB secrets | Full data compromise |

## 2. Trust boundaries (target)

```
Browser (untrusted)  ⇄  Next.js / FastAPI edge  ⇄  App services  ⇄  Postgres / Storage
   anon key + session     validate + authz           least-privilege roles
```

- Browser may hold the **public** anon key and the user session only.
- **Service-role key is server-side only.**
- Every API request is untrusted, including authenticated ones.

## 3. As-is posture (terminal app)

Acceptable for a local assignment; **not** for a hosted product:

- Binds `127.0.0.1` only; no TLS; no authentication.
- JSON list over TCP; 10 MiB cap; exceptions returned as `{ok:false, error}`
  with exception type and message (information leak if ever exposed).
- Double-bind probe prevents a silent second server on Windows.
- No logging policy, no secret management, no `.gitignore`.

## 4. Authentication requirements

- S-1 Email/password: hashed by the IdP (Supabase Auth in the default proposal);
  verification + reset; no custom crypto. Figma shows email verification after
  sign-up and a **minimum 8-character** hint `[figma-obs]`; exact policy is still
  an owner decision (Q9). Generic credential errors match the Figma copy
  “The email or password isn’t right.”
- S-2 Google OAuth (OIDC): `state` / PKCE; validate issuer/audience/expiry.
- S-3 GitHub OAuth: handle private/missing email explicitly.
- S-4 Sessions: short-lived access, refresh, revocation, logout-everywhere.
  Cookie vs bearer is **D-4**. If cookies: `httpOnly`, `Secure`, `SameSite`.
- S-5 Account linking only after verified email ownership (**D-2**).
- S-6 Rate-limit sign-in/reset; generic errors (limit user enumeration).
- S-7 MFA out of Phase 1; do not block it in the data model.

## 5. Authorization

- S-8 RLS on every user-owned table; default deny; tests for cross-user denial.
- S-9 API enforces ownership independently of the database.
- S-10 No IDOR on dataset/report/share IDs. Prefer 404 over 403 for other users’
  resources (existence hiding — confirm at implementation).
- S-11 Storage paths namespaced by `user_id`; no public buckets by default.

## 6. Input validation and abuse

- S-12 CSV: max size/rows; headers must match INV-9; typed coercion.
- S-13 Missing/negative readings are invalid rows (INV-10), not 500s.
- S-14 Body size limits at the edge.
- S-15 Export injection: neutralize `= + - @` (and tab/CR) in CSV cells; HTML-escape.
- S-16 Sanitize filenames; no path traversal in storage keys.
- S-17 Duplicate-upload policy is product-open; checksums are still useful.

## 7. Transport and platform

- S-18 TLS; HSTS in production.
- S-19 CSP, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`,
  frame ancestors none/self.
- S-20 CSRF protection if using cookie sessions (D-4).
- S-21 CORS allow-list; no wildcard + credentials.

## 8. Secrets

- S-22 Env / secret manager only; never commit `.env`.
- S-23 Separate keys per environment.
- S-24 App DB role is not superuser; service role unused in the browser.
- S-25 `.gitignore` must exclude env files, caches, build output (Stage 1).

## 9. Privacy

- S-26 Treat customer names and consumption as personal data.
- S-27 TLS in transit; managed encryption at rest.
- S-28 Retention + user-initiated delete (cascade documented).
- S-29 Store only what analysis and history need.
- S-30 No PII in logs.
- S-31 Residency recorded when D-1 is decided.

## 10. Supply chain and operations

- S-32 SCA + SAST in CI; block high/critical where practical.
- S-33 Lockfiles; license review for new deps.
- S-34 Human review for auth, RLS, crypto, export.
- S-35 Abuse testing before public launch (auth, upload, IDOR).
- S-36 Log auth events and denials without PII.
- S-37 Alert on login/upload anomalies.
- S-38 Incident path: contain → rotate → notify → postmortem.

## 11. Gaps vs current code (tracked in TASKS)

| Gap | Planned stage |
|---|---|
| Exception strings echoed to clients | Stage 2 |
| No auth | Stage 3 |
| No RLS / ownership | Stages 4–5 |
| No upload caps | Stage 4 |
| No TLS/headers/rate limits | Stage 7 |
| No `.gitignore` / secret hygiene | Stage 1 and 7 |

## 12. OWASP Top 10 checklist (Phase 1 — all unchecked until done)

- [ ] A01 Broken access control
- [ ] A02 Cryptographic failures
- [ ] A03 Injection
- [ ] A04 Insecure design (this document is the starting threat model)
- [ ] A05 Security misconfiguration
- [ ] A06 Vulnerable components
- [ ] A07 Identification and authentication failures
- [ ] A08 Software and data integrity failures
- [ ] A09 Security logging and monitoring failures
- [ ] A10 SSRF — Phase 1 should not fetch user-supplied URLs
