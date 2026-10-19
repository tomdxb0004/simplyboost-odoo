import re

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

# A SimplyBoost bot ID is a UUID; anything else is a typo and would load a
# widget that cannot find its bot.
BOT_ID_PATTERN = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')

WIDGET_URL = 'https://get.simplyboost.io/widget.js'
# Lets a test database point at a non-production widget. Only https addresses
# are used, so the parameter cannot load a script over plain http.
WIDGET_URL_PARAMETER = 'website_simplyboost.widget_url'


class Website(models.Model):
    _inherit = 'website'

    simplyboost_bot_id = fields.Char(
        string='SimplyBoost Bot ID',
        help='The ID of the chatbot to show on this website. In the SimplyBoost dashboard it is '
             'under Channels, Website.',
    )
    simplyboost_data_consent = fields.Boolean(
        string='Send visitors\' chat messages to SimplyBoost',
        help='The chat runs on SimplyBoost\'s servers: what visitors type in the chat, the contact '
             'details they enter in its contact form and their ratings of replies are sent to '
             'SimplyBoost to answer them. Nothing is sent until this is ticked.',
    )

    @api.constrains('simplyboost_bot_id')
    def _check_simplyboost_bot_id(self):
        for website in self:
            bot_id = website._normalised_simplyboost_bot_id()
            if website.simplyboost_bot_id and not bot_id:
                raise ValidationError(_(
                    'The SimplyBoost Bot ID looks like xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx. '
                    'Copy it from Channels, Website in your SimplyBoost dashboard.'
                ))

    def _normalised_simplyboost_bot_id(self):
        self.ensure_one()
        bot_id = (self.simplyboost_bot_id or '').strip().lower()
        return bot_id if BOT_ID_PATTERN.match(bot_id) else False

    def _simplyboost_bot_id_to_render(self):
        """The bot ID to put on this website's pages, or False to add nothing:
        the chat loads only with a valid ID and the owner's consent."""
        self.ensure_one()
        if not self.simplyboost_data_consent:
            return False
        return self._normalised_simplyboost_bot_id()

    def _simplyboost_widget_url(self):
        url = self.env['ir.config_parameter'].sudo().get_param(WIDGET_URL_PARAMETER) or ''
        return url if url.startswith('https://') else WIDGET_URL
