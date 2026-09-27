# Database readiness — frontend contract

## Current deployment

GitHub Pages remains the static frontend. `assets/data-store.js` is the only boundary for checklist and CV draft storage. It currently uses the existing browser keys `mbo_phase1_v1` and `mbo_cv_draft_v1`; no data leaves the browser. The removed “My Space” code used `mbo_phase2_v1` for favorites and history. Do not erase that legacy key from visitors' browsers before users have a reviewed migration option. The site does not presently offer favorites/history UI, accounts, sync, remote notifications or real visitor totals.

## Proposed backend contract (not live)

Host an HTTPS API separately from GitHub Pages. Authenticate users with a managed identity provider, then authorize every request against the authenticated subject on the server. Never accept a user ID supplied by the browser as proof of ownership. Restrict CORS to the production Pages origin and configured preview origins. Use short-lived sessions, rate limits, CSRF protection where cookies are used, and server-side input limits. No database credentials or service-role tokens go into the repository or browser.

| Resource | Operations | Example fields |
| --- | --- | --- |
| `GET/PUT /v1/me/checklist` | Fetch or replace the signed-in user's checklist | `version`, `checks` (known task IDs only), `updatedAt` |
| `GET/PUT /v1/me/favorites` | Fetch or replace article URLs saved by the user | canonical article IDs, `updatedAt` |
| `GET/PUT /v1/me/history` | Optional, explicit opt-in | article IDs, last-read timestamp |
| `GET /v1/content/updates` | Published bilingual updates only | stable ID, Arabic/Dutch text, official source, verified date |
| `POST /v1/admin/content` | Editor-only publishing after review | bilingual content, sources, revision, status |

Database records should have unique `(user_id, item_id)` keys for favorites and checklist items, timestamps, and server authorization rules. Source URLs and verification dates belong to content records. Public visitor counts need a server-side counting definition and abuse controls before display.

## Migration and privacy

At sign-in, show the user a preview of local progress and offer an explicit import; merge by stable task/article IDs, not page titles. Keep the local copy until the server confirms a successful write. Provide export and deletion routes. Do not silently import the old `mbo_phase2_v1` key. CV drafts contain direct contact details: keep them device-local for now; any later cloud CV storage must be a separate explicit opt-in with a clear retention/deletion policy. Do not store BSN, permit numbers or uploaded identity documents in the initial schema.

## Content workflow

Use a Git-backed bilingual content schema and a build step that emits static HTML at the current article paths. Preserve canonical URLs, sitemap, structured data, Google tags and human review of official sources. Adding the backend does not require migrating page rendering away from GitHub Pages.

## Activation gate

Before configuring a live API: choose a hosting/auth provider, define the privacy policy and retention period, review the schema and threat model, then implement and test the authenticated API. Only then switch `data-store.js` to remote reads/writes for signed-in users while retaining the local adapter for guests and offline access. Never infer that a backend is active because this document or adapter exists.
