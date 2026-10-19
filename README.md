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

## A data module: no Python

Odoo Online (Odoo's hosted SaaS, where most small businesses are) installs
Apps Store modules only when they contain no Python: XML, CSV and `static/`
files. So this module has none. The two settings are custom fields declared
in `data/ir_model_fields.xml` (`x_simplyboost_bot_id` and
`x_simplyboost_data_consent` on `website`, plus related copies on
`res.config.settings` for the settings screen), and the Bot ID check is in
the QWeb template: the script is added only when the consent box is ticked and
the Bot ID is shaped like a UUID (spaces and capitals are ignored). A badly
pasted Bot ID is not refused when saving, it just loads nothing. **Adding any
`.py` file makes the app unavailable on Odoo Online.** The same module installs
on Odoo.sh and self-hosted Odoo.

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
folder is published on its own to the public repository
`tomdxb0004/simplyboost-odoo`, branches `18.0`, `19.0` and `20.0`. The files
are the same for every series; only `version` in the manifest starts with the
series. This folder stays the only source (it holds `18.0.x`); publish with:

```bash
git subtree split --prefix integrations/odoo -b odoo-publish
git push --force https://github.com/tomdxb0004/simplyboost-odoo.git odoo-publish:18.0
for v in 19.0 20.0; do
  git worktree add -q /tmp/odoo-$v odoo-publish --detach
  sed -i '' "s/'version': '18\.0\./'version': '$v./" /tmp/odoo-$v/website_simplyboost/__manifest__.py
  git -C /tmp/odoo-$v commit -qam "Odoo $v"
  git -C /tmp/odoo-$v push --force https://github.com/tomdxb0004/simplyboost-odoo.git HEAD:$v
  git worktree remove --force /tmp/odoo-$v
done
git branch -D odoo-publish
```

Bump the last part of `version` with every release (the store needs a new
number to update). Then register each branch at apps.odoo.com/apps/upload:
`ssh://git@github.com/tomdxb0004/simplyboost-odoo.git#18.0`, `#19.0`, `#20.0`.
The settings block is placed after `website_info_settings`, which 18.0, 19.0
and 20.0 all have.

The description page shows two screenshots from a real Odoo 18 with this module
(`screenshot_chat.png`, `screenshot_settings.png`). Retake them when the
settings or the widget change.

## Checking a change

There are no Python tests (they would make it a Python module). Check a change
in a throwaway Odoo of each series the way Odoo Online loads it: import the
module as a zip (`base_import_module`), then in Website → Configuration →
Settings set a Bot ID without consent (no script on the homepage), tick consent
(one `<script id="simplyboost-classic-script" … data-bot-id="…">`), and try a
malformed Bot ID (no script).
