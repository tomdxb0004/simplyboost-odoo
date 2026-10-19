from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    simplyboost_bot_id = fields.Char(related='website_id.simplyboost_bot_id', readonly=False)
    simplyboost_data_consent = fields.Boolean(related='website_id.simplyboost_data_consent', readonly=False)
