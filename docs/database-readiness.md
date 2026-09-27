# Database and backend readiness

## Current state

The frontend is GitHub Pages. Browser-only storage remains the default for checklist and CV draft. Firebase project `gidsnederland-35a81` has been configured by its owner with Firestore Standard, Google Authentication and the GitHub Pages hostname. Optional checklist sync code and strict rules are in this repository, but the owner must publish the rules in Firebase Console before sync is usable. See `docs/firebase-setup.md`.

No live news CMS, company registration workflow, visitor counter API, payments, alerts, or public user profiles are active.

## Data boundaries

| Data | Initial storage | Public? | Rule |
| --- | --- | --- | --- |
| Task checklist | `/users/{uid}/checklist/current` in Firestore | No | Owner only; explicit sync action; fixed known task IDs |
| CV draft | Browser storage | No | Never cloud upload in initial release |
| Articles and news | Git-backed bilingual Markdown/JSON | Published output only | Human review, sources and timestamps; static HTML build |
| Provider application | Future private application record | No | Applicant can edit pending fields only; admin review required |
| Approved provider profile | Future public listing collection/build | Yes, selected fields | Admin-created/approved; applicant cannot publish or self-verify |
| Visitor metric | Future protected counter API | Aggregate only | No browser write access to a shared total; define measurement and abuse limits |

## Dashboard workflow

The editorial dashboard must authenticate authors and send changes through a review/publish workflow. GitHub repository write tokens remain server-side or within the trusted CMS integration; never expose them in browser JS. The publish step runs a static build that produces SEO-ready HTML, canonical URLs, Article/NewsArticle or FAQ schema only where justified, bilingual metadata and sitemap entries while preserving existing routes.

News records should include ID, category, Arabic/Dutch title and summary, affected audience, practical consequence, official source, source date, effective date, verification date, status (`confirmed`, `announced`, `proposed`), reviewer and publication state. Do not present an announcement or proposal as a policy already in effect.

Company records must distinguish private applicant details from approved public listing fields. Establish verification, consent, complaint, correction/deletion and retention procedures before opening registration. Initially do not process payments, store identity documents, or advertise tax/immigration credentials without verification.

## Visitor count design gate

Do not use a browser-side Firestore increment for a public total. A trustworthy count needs a server endpoint, bot/rate-abuse controls and a definition (pageviews vs. deduplicated visits); describe any identifiers and retention in the privacy notice. Firebase Cloud Functions requires the Blaze plan, so it is not a strict Spark-only choice. Evaluate a free external Worker/DB or privacy-oriented analytics service and its current limits before implementation.

## Privacy and account controls

Guests continue to use the site without signing in. Google login is for optional website sync and has no connection to DigiD. Provide local export/deletion and an in-product account/cloud deletion route. Collect no BSN, permit number, uploaded identity document, or cloud CV in the first release. Keep policy wording aligned with actual Firebase region, fields, purpose and retention.
