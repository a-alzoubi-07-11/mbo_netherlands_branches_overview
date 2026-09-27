# Firebase checklist sync

## Firebase project

- Project: `gidsnederland-35a81`
- Cloud Firestore Standard: created in the project; use the default `(default)` database.
- Firebase Authentication: Google provider enabled.
- GitHub Pages origin `a-alzoubi-07-11.github.io`: added to authorized domains.
- Web configuration is in `assets/firebase-sync.js`. Firebase web API keys identify the project and are public by design; they do not authorize database access. Keep service-account private keys out of this repository.

## What the website stores

Only the Phase 1 checklist may be synced, after the visitor explicitly signs in and chooses **merge this device with account**. Data is stored at `/users/{uid}/checklist/current` with the known checklist task IDs and an update timestamp. The upload merges checked tasks; it does not clear completed tasks. Download explicitly replaces the current device's checklist. The user can delete the site account and its cloud checklist from the same panel. The Google account itself is not deleted. CV drafts remain local and are never uploaded. Visitors can use the site without an account or DigiD.

## Publish secure rules before enabling sync

The repository file `firestore.rules` allows a signed-in user to read, write and delete only their own `current` checklist; it validates allowed fields/task IDs and defaults every other path to deny. Before asking visitors to sync:

1. In Firebase Console open **Firestore Database → Rules**.
2. Replace the console rules with the complete contents of `firestore.rules` and click **Publish**.
3. In Authentication → Settings verify `a-alzoubi-07-11.github.io` is listed as an authorized domain.
4. Test sign-in and checklist read/write as one user, then verify a different signed-in user cannot access that path.
5. Verify upload, download, sign-out, account deletion, Arabic and Dutch UI, and mobile layout.

The default rules created with the database denied all access. Until the scoped rules above are published, checklist reads and writes should fail closed; do not use test-mode rules.

## Data protection and future expansion

Cloud synchronization is optional. The privacy page describes Firebase authentication data, the checklist fields, region, and deletion control. Review the privacy notice and Firebase terms for the site's operation before inviting users. Do not add BSN, permit numbers, identity documents, or CV contact details to this initial database. Future Android/iOS apps can register additional Firebase app IDs in this project and use the same Firestore database and Authentication service.

Firestore's Spark plan has daily free quotas. Monitor the Firebase usage page; avoid page-wide realtime listeners. Add content management, analytics, and visitor metrics as separate reviewed features rather than putting them in the personal checklist database.
