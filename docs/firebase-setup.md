# Firebase connection plan (not active)

GitHub Pages remains the frontend. Use **Firebase Cloud Firestore**, on the Spark plan, with Firebase Authentication for optional account sync. DigiD is an identity service for Dutch government services and is not a login method for this site. Guests must retain access and local checklist/CV storage.

## Before activation

1. Create a Firebase project owned by the site operator, choose the Spark plan and one Firestore database in a suitable European region. Register a web app and add `a-alzoubi-07-11.github.io` to Authentication authorized domains.
2. Enable a chosen sign-in provider (for example Google account), then implement explicit sign-in and sign-out with bilingual consent, deletion and export. Never request DigiD credentials or BSN. Anonymous per-device identities do not provide cross-device sync.
3. Replace the *deny-all* `firestore.rules` with narrowly scoped rules for `/users/{uid}/checklist/current` only. Require `request.auth.uid == uid`, validate allowed task IDs and booleans, prohibit extra fields, limit document size, and test reads/writes by two different users in the Firebase emulator before publishing rules. Default-deny all other paths.
4. Add the Firebase **web app config** only after rules are published. The web config identifies the project and is public; never publish service-account credentials, Admin SDK keys, or a broadly writable database. Connect a new optional sync adapter to `assets/data-store.js`. Do not upload local data automatically: show a preview and ask before importing. Retain the local copy until remote confirmation.
5. Update both language versions of `privacy.html` before collecting account data: controller, Firebase processing, purposes and legal basis, fields, storage region and transfers, retention period, deletion/export route, and contact. Test Arabic/Dutch and mobile/desktop before enabling sync.

Current commit contains only deny-all rules and a deployment plan. It does **not** connect a Firebase project, create accounts, or transmit CV drafts. The current public site works without a database. The operator must provide the Firebase web app config and project access to activate it.

Firestore's one free database includes 1 GiB storage, 50,000 document reads/day, 20,000 writes/day and 20,000 deletes/day; monitor usage and the current Firebase pricing page before launch. Firestore rules, rather than an obscured client configuration, enforce access control. Avoid realtime listeners on every page to keep within the free quota.
