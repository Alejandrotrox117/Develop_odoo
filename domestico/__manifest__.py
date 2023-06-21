# -*- coding: utf-8 -*-
{
    'name': "domestico",
    'author': "My Company",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base','product', 'account', 'contacts', 'sale'],
    'data': [
        'security/domestico_groups.xml',
        # 'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'views/product_template_view.xml',
        'views/account_move_form_custom.xml',
        'views/account_payments_view.xml',
        # 'views/product_template_view.xml',
        'views/domestico_menus.xml',
        ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
