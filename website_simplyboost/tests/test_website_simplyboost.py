from odoo.exceptions import ValidationError
from odoo.tests import HttpCase, TransactionCase, tagged

BOT_ID = '6f1c2a9e-3b4d-4e5f-8a7b-0c1d2e3f4a5b'


class TestBotIdAndConsent(TransactionCase):

    def setUp(self):
        super().setUp()
        self.website = self.env['website'].create({'name': 'SimplyBoost test site'})

    def test_a_bot_id_that_is_not_a_bot_id_is_refused(self):
        for value in ('abc', '6f1c2a9e3b4d4e5f8a7b0c1d2e3f4a5b', BOT_ID + 'x', '<script>'):
            with self.subTest(value=value), self.assertRaises(ValidationError):
                self.website.write({'simplyboost_bot_id': value})

    def test_spaces_and_capitals_from_a_copy_paste_are_accepted(self):
        self.website.write({'simplyboost_bot_id': f'  {BOT_ID.upper()} ', 'simplyboost_data_consent': True})
        self.assertEqual(self.website._simplyboost_bot_id_to_render(), BOT_ID)

    def test_nothing_is_added_without_consent(self):
        self.website.write({'simplyboost_bot_id': BOT_ID, 'simplyboost_data_consent': False})
        self.assertFalse(self.website._simplyboost_bot_id_to_render())

    def test_nothing_is_added_without_a_bot_id(self):
        self.website.write({'simplyboost_bot_id': False, 'simplyboost_data_consent': True})
        self.assertFalse(self.website._simplyboost_bot_id_to_render())

    def test_only_an_https_widget_address_replaces_the_default(self):
        parameters = self.env['ir.config_parameter'].sudo()
        parameters.set_param('website_simplyboost.widget_url', 'http://example.com/widget.js')
        self.assertEqual(self.website._simplyboost_widget_url(), 'https://get.simplyboost.io/widget.js')
        parameters.set_param('website_simplyboost.widget_url', 'https://staging.example.com/widget.js')
        self.assertEqual(self.website._simplyboost_widget_url(), 'https://staging.example.com/widget.js')


@tagged('post_install', '-at_install')
class TestWidgetOnPages(HttpCase):

    def setUp(self):
        super().setUp()
        self.website = self.env['website'].get_current_website()

    def _homepage(self):
        response = self.url_open('/')
        self.assertEqual(response.status_code, 200)
        return response.text

    def test_the_widget_is_on_the_page_once_configured(self):
        self.website.write({'simplyboost_bot_id': BOT_ID, 'simplyboost_data_consent': True})
        page = self._homepage()
        self.assertIn('id="simplyboost-classic-script"', page)
        self.assertIn(f'data-bot-id="{BOT_ID}"', page)
        self.assertIn('src="https://get.simplyboost.io/widget.js"', page)

    def test_the_widget_is_not_on_the_page_without_consent(self):
        self.website.write({'simplyboost_bot_id': BOT_ID, 'simplyboost_data_consent': False})
        self.assertNotIn('simplyboost-classic-script', self._homepage())
