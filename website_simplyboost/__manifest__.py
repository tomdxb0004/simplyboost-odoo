{
    'name': 'AI Support Agent',
    'version': '18.0.1.0.0',
    'summary': 'AI support agent and product specialist on your website, connected to your CRM and helpdesk through SimplyBoost',
    'description': 'Adds your SimplyBoost AI agent to your Odoo website. Requires a SimplyBoost account.',
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
