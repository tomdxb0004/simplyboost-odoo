# Odoo app: Website AI Chatbot (`website_simplyboost`)

Adds the SimplyBoost chat widget to an Odoo website. The owner pastes the
chatbot's Bot ID in Website → Configuration → Settings → AI Chatbot and ticks
the consent box; every page of that website then loads

```html
<script src="https://get.simplyboost.io/widget.js" id="simplyboost-classic-script" async data-bot-id="…"></script>
```

at the end of `<body>`. The widget starts from the `data-bot-id` attribute
(`frontend-dashboard/src/widget/main.jsx`), so the page carries no inline
script. Each Odoo website has its own Bot ID.

## What is and is not in this module

Only the code above. It holds no SimplyBoost secrets and calls no SimplyBoost
API: everything Odoo sees (Odoo S.A. scans the repository; buyers get the
source) is public. Keep it that way; a later version that syncs contacts must
use the customer's own `/api/v1` token, entered in their Odoo.

## Rules it follows (Odoo Apps vendor guidelines)

- Name ≤ 25 characters, no company name; LGPL-3; English description page in
  `static/description/index.html` with Bootstrap classes only, no scripts and
  no external links (a `mailto:` is allowed).
- The external service and the data sent are stated on the description page and
  in the settings, and nothing loads until the owner ticks the consent box.
- Icon `static/description/icon.png`, cover `static/description/banner.png`
  (manifest `images`).

## Publishing

The Odoo Apps store reads a Git repository with one folder per module at its
root and one branch per Odoo series. Do not register this repository: publish
the module from its own repository.

1. Create a repository (e.g. `simplyboost-odoo`) with `website_simplyboost/`
   at its root, on a branch named `18.0`.
2. Before registering, add screenshots of the settings and of the chat on an
   Odoo website to `static/description/` and show them on `index.html`; the
   store ranks pages without them lower.
3. Register it at apps.odoo.com/apps/upload as
   `ssh://git@github.com/<org>/simplyboost-odoo.git#18.0` (a private repository
   needs Odoo's deploy key).
4. For Odoo 19, add a `19.0` branch with `version` starting `19.0.`. The
   settings block is placed after `website_info_settings`, which both 18.0 and
   19.0 have.

## Odoo Online

Odoo Online (Odoo's hosted SaaS) does not install third-party modules that
contain Python, so this app serves Odoo.sh and self-hosted Odoo. On Odoo
Online the owner pastes the dashboard's install snippet into Website →
Configuration → Settings → Custom Code instead.

## Tests

`tests/test_website_simplyboost.py` (Bot ID check, consent, widget address, the
script on the homepage). Run them in an Odoo 18 instance:

```bash
odoo-bin -d <test db> -i website_simplyboost --test-tags /website_simplyboost --stop-after-init
```
