# -*- coding: utf-8 -*-
{
    'name': "Saaf Account Dynamic Reports",

    'summary': """
        Saaf Account Dynamic Reports""",

    'description': """
        Saaf Account Dynamic Reports
    """,

    'author': "islam megger",
    'website': "http://projomania.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account_dynamic_reports','dynamic_xlsx'],

    # always loaded
    'data': [
        'views/partner_ledger_view.xml',
    ],
    'qweb': ['static/src/xml/view.xml'],
}