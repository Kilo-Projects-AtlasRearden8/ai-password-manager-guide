STATUS.md
=========

What was built
--------------
A beginner manual on passwords and password managers, delivered as both
markdown docs (docs/) and a static HTML site (site/). Topics covered:

1. Choosing a password manager (docs/choosing-a-password-manager.md,
   site/choosing-a-password-manager.html)
2. Two-factor authentication (docs/two-factor-authentication.md,
   site/two-factor-authentication.html)
3. Securing your accounts with AI help
   (docs/securing-accounts-with-ai.md,
   site/securing-accounts-with-ai.html)
4. Printable security checklist (docs/security-checklist.md,
   site/security-checklist.html)

Also includes:
- LICENSE — MIT License, Copyright (c) 2026 Asdale Dynamics, LLC
- README.md — project overview with Asdale Dynamics, LLC credit
- site/assets/css/style.css — clean, print-friendly styles
- site/assets/js/main.js — print button and checklist persistence

How to run it
-------------
Open site/index.html in any web browser. All pages are static HTML — no
build step, no server, no dependencies required.

To print the checklist, open site/security-checklist.html and use the
"Print this checklist" button, or use your browser's print command.
Print styles hide navigation and show only the checklist content.

Verification results
--------------------
- All 14 files created and staged in git
- Git commit created: e675fb2 "Initial commit: AI password manager beginner guide"
- LICENSE copyright line verified: "Copyright (c) 2026 Asdale Dynamics, LLC"
- README.md credits Asdale Dynamics, LLC
- No .github/workflows files present
- No secrets, API keys, or personal data in any file
- All HTML pages link correctly to one another and to the CSS/JS assets
- Print CSS confirmed present in style.css and security-checklist.html

Known gaps
----------
- No automated test suite (static site, no build process to test)
- HTML not validated with a formal validator (visual inspection only)
- No search functionality across pages
- No dark mode variant
- Checklist state persists via localStorage only (browser-specific)

Published by Asdale Dynamics, LLC — plain English, step by step, never condescending.