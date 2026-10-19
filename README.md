# Odoo app: AI Support Agent (`website_simplyboost`)

Puts a SimplyBoost agent (support agent and product specialist) on an Odoo
website. The owner pastes the agent's Bot ID in Website → Configuration →
Settings → AI Support Agent and ticks the consent box; every page of that
website then loads

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
root and one branch per Odoo series. It must not read this repository, so this
folder is published on its own to the private repository
`tomdxb0004/simplyboost-odoo`, branch `18.0`. This folder stays the only source;
publish with:

```bash
git subtree split --prefix integrations/odoo -b odoo-18.0-publish
git push https://github.com/tomdxb0004/simplyboost-odoo.git odoo-18.0-publish:18.0
git branch -D odoo-18.0-publish
```

Then register `ssh://git@github.com/tomdxb0004/simplyboost-odoo.git#18.0` at
apps.odoo.com/apps/upload (a private repository needs Odoo's deploy key added
to it on GitHub). For Odoo 19, add a `19.0` branch with `version` starting
`19.0.`; the settings block is placed after `website_info_settings`, which both
18.0 and 19.0 have.

The description page shows two screenshots from a real Odoo 18 with this module
(`screenshot_chat.png`, `screenshot_settings.png`). Retake them when the
settings or the widget change.

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
