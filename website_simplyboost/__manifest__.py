{
    'name': 'AI Agent: Support & Leads',
    'version': '19.0.1.2.0',
    'summary': 'AI chatbot for customer support and lead generation on your Odoo website. Answers from your own content, captures leads and hands over to your team.',
    'description': 'SimplyBoost AI agent (AI chatbot) for customer support and lead generation on your Odoo website. Works on Odoo Online, Odoo.sh and on-premise. Requires a SimplyBoost account.',
    'category': 'Website/Website',
    'author': 'SimplyBoost',
    'license': 'LGPL-3',
    'support': 'support@simplyboost.io',
    'depends': ['website'],
    'data': [
        'data/ir_model_fields.xml',
        'views/res_config_settings_views.xml',
        'views/website_templates.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
}
