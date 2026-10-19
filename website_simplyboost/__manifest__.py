{
    'name': 'Website AI Chatbot',
    'version': '18.0.1.0.0',
    'summary': 'An AI assistant on your Odoo website that answers visitors from your own content',
    'description': 'Adds the SimplyBoost chat widget to your Odoo website. Requires a SimplyBoost account.',
    'category': 'Website/Website',
    'author': 'SimplyBoost',
    'license': 'LGPL-3',
    'support': 'support@simplyboost.io',
    'depends': ['website'],
    'data': [
        'views/res_config_settings_views.xml',
        'views/website_templates.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
}
