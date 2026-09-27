# Site audit — 27 September 2026

## Implemented

- Removed all Phase 2/My Space assets and references in the preceding release. The new service worker uses network-first requests, clears old `mbo-netherlands-*` caches on activation, and provides `/refresh.html` to clear project caches on an affected device. Previous browser-local favorites/history remain untouched.
- Optional Google Analytics and Gabster scripts now load only after an explicit choice. Reject and accept have equal prominence; settings may be changed from the page footer. AdSense publisher ID, `ads.txt`, Analytics ID, GTM ID and verification meta are retained. AdSense and GTM execution is paused while Google consent and container configuration are independently checked. No noscript GTM iframe runs before a choice.
- Privacy information is available in Arabic and Dutch. Contact uses the visitor's email application; CV and checklist state remain in local browser storage.
- `scripts/audit-links.py` verifies local static targets and sitemap paths. Seven article pages receive an official reference link through the shared article renderer. The index WebSite structured-data URLs and the project sitemap reference were corrected.

## Official destination references checked against current primary search results

| Topic | Destination |
| --- | --- |
| DigiD application | https://www.digid.nl/en/apply-and-activate |
| NT2 Program I | https://www.duo.nl/particulier/staatsexamen-nt2/hoe-het-staatsexamen-nt2-werkt.jsp |
| Employment contracts | https://www.rijksoverheid.nl/themas/werk/arbeidsovereenkomst-en-cao |
| Childcare allowance | https://www.belastingdienst.nl/wps/wcm/connect/nl/kinderopvangtoeslag/content/hoe-moet-ik-kinderopvangtoeslag-aanvragen |
| Asylum family reunification | https://ind.nl/en/residence-permits/asylum/asylum-family-reunification |
| Permanent residence | https://ind.nl/en/replace-extend-renew-and-change/permanent-residency/permanent-residence-permit |
| Newcomer checklist | https://www.rijksoverheid.nl/vraag-en-antwoord/immigratie-naar-nederland/wat-moet-ik-regelen-als-ik-in-nederland-kom-wonen |
| MBO search | https://www.kiesmbo.nl/opleidingen |
| Work for non-EU nationals | https://www.uwv.nl/en/individuals/working-in-the-netherlands/non-eu-eea-or-swiss-national |

External links to social media or independent education portals cannot be guaranteed permanently; providers may change routes or restrict automated access. Re-run the local script after changing a page. The official links above are navigational references, not proof that every article's legal details are current.

## Outstanding checks before claiming legal compliance

1. Review the AdSense account's European regulations message/CMP and the GTM container's tags with an appropriate certified solution. Keep ads and GTM paused until complete. Verify any contracts and cross-border transfer disclosures for each chosen processor.
2. Have the privacy text, retention criteria, rights-handling practice, contact identity, and content of immigration, tax and employment articles checked by a qualified Dutch privacy/legal specialist. Publisher must implement the retention practice described on the page.
3. `robots.txt` and `ads.txt` in this *project* repository are served under `/mbo_netherlands_branches_overview/`; crawlers may request domain-root files at `https://a-alzoubi-07-11.github.io/robots.txt` and `/ads.txt`. This requires review in the domain-root Pages repository or a custom domain.
4. Check Google Analytics property configuration and whether any tag still collects data before consent via the Google account or other repositories. The repository audit cannot inspect those account settings.
