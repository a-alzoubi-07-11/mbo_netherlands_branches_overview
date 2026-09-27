# Phase 3 — Personal portal and service platform

## Current project

The project remains a static GitHub Pages website. `mbo_site_lang` controls the full Arabic RTL / Dutch LTR interface. Phase 1 owns the browser checklist (`mbo_phase1_v1`); Phase 3 recommends the next task. CV drafts remain local. My Space was removed; its legacy key `mbo_phase2_v1` is not silently imported.

Firebase project `gidsnederland-35a81` now has a Standard Firestore database, Google sign-in and the GitHub Pages domain registered (confirmed from the owner's console screenshots). The site code is being prepared for optional checklist sync. It is not production-ready until the owner publishes the scoped `firestore.rules` and tests two separate accounts. Google sign-in is optional; DigiD is never used for this site.

## Product direction

Serve people already in the Netherlands and people planning to arrive. Let visitors start without an account; offer optional account sync for personal progress. Add a company-provider directory, an editorial dashboard and a reviewed daily updates feed as separate modules.

### 1. Personal account and checklist

Store only the selected user's checklist at `/users/{uid}/checklist/current`. The user explicitly connects Google, then separately chooses upload/merge or download. CV, BSN, permit numbers and identity documents stay out of the first database. `firestore.rules` allows a user to access only their own checklist and denies every other path.

### 2. Articles and newsroom dashboard

Keep editorial content in bilingual Markdown/JSON in Git, managed through a secure `/admin/` CMS with draft → review → approved → published states. Use GitHub Actions to render reviewed content to static HTML and update sitemap/schema. Preserve all existing article URLs and Google metadata. Decap CMS is one candidate, but GitHub Pages cannot host its OAuth secret or repository write credential; select and secure the authentication/publishing bridge before building the dashboard. Do not put a GitHub token in browser JavaScript.

Each update has a stable ID, category, Arabic and Dutch title/summary, who is affected, practical action, official source URL, source publication date, effective date, verification date, reviewer, and status (confirmed / announced / proposed). Put confirmed, relevant items in a compact homepage news strip linked to a readable detail page. Pause automatic movement for accessibility; no unreviewed generated news goes live.

Initial newsroom sections: IND/asylum/residence, DUO and education, government allowances/support/financing, work and tax, and essential daily-life changes. The editor verifies each summary against an official government source and separates a proposal from a decision that has taken effect.

### 3. Company and service-provider directory

Build a provider application and an Arabic/Dutch directory for services such as bookkeeping, tax preparation, translation, education support and other newcomer services. An applicant's profile stays private and `pending` until reviewed. Only approved directory records are public. Providers cannot approve themselves or change their verification status from the browser. Start with listings and direct contact; defer payments, bookings, reviews and claims of official accreditation until moderation, consumer terms, qualification checks and complaint handling are designed.

Before collecting company contact/person data, define which details are public, obtain explicit publication consent, set deletion/retention rules, and publish provider terms and a clear statement of the website's role. Do not imply that listed providers are government agencies. Verify regulated or credentialed claims before showing them.

### 4. Cumulative visitor count

The previous embedded counter request was removed: it depended on an external counter API but had no matching `visitorCount` display element, and its fallback counted browser-local page loads rather than site-wide visits. Do not increment a public Firestore document directly from browsers; visitors could forge totals. Define whether the displayed metric is page views or deduplicated visits, then use a protected server endpoint, privacy notice and abuse controls. Firebase Cloud Functions deployment requires Blaze billing; if staying strictly free, evaluate a separate free Worker/database or privacy-oriented analytics provider before selecting one.

## Deployment model

- Static pages, article pages, sitemap and public newsroom output: GitHub Pages.
- Personal checklist/authentication: Firebase Auth + Firestore, optional and narrowly scoped.
- Editorial dashboard: Git-backed content + secured authoring workflow + GitHub Actions static build.
- Company applications: private, moderated records; public read-only approved profiles.
- Visitor counter: separate protected service if a visible aggregate is retained.

This keeps the app and future custom domain independent from Firestore. Android/iOS apps can register additional Firebase clients later and share the same Auth/Firestore project with the website.
