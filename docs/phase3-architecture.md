# Phase 3 architecture

## Current static release

GitHub Pages serves the existing HTML pages. Phase 1 owns the task checklist in `mbo_phase1_v1`. The former Phase 2 panel has been removed; its browser key `mbo_phase2_v1` is retained only in visitor storage for a future, consent-based import. Phase 3 reads Phase 1 progress and recommends the next task, without creating a second checklist. Language selection continues through `mbo_site_lang`. All progress remains on this device; no account, synchronization, personalized alerts or real visitor total is claimed.

## Backend migration path

1. Add a separately hosted API with managed authentication and a database. Use authenticated sessions, server-side authorization, and per-user records for checklist progress and favorites. Keep secrets and database credentials on the server. Offer an explicit import of existing browser storage after sign-in, with a preview of what will be uploaded.
2. Move articles to a Git-backed content workflow with editorial review, bilingual fields, official-source URLs and verified update dates. Generate static HTML and sitemap at build time, preserving existing URLs, canonical links, schema, and AdSense tags. Do not replace the seven current article URLs during migration.
3. Add update subscriptions, verified analytics and a visitor counter only when server-side collection, abuse controls, privacy information and measurement definitions are established. Never represent browser-local counts as site-wide traffic.

Keep GitHub Pages as the frontend initially. Serve the API from a separate HTTPS origin with restricted CORS, rate limits and data export/deletion. Avoid collecting immigration documents or identity numbers in the first release.

See `docs/database-readiness.md` for the draft API contract and migration gates.
