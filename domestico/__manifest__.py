# -*- coding: utf-8 -*-
{
    'name': "domestico",
    'author': "My Company",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base','product', 'stock', 'account', 'contacts', 'sale'],
    'data': [
        'security/domestico_groups.xml',
        'security/ir.model.access.csv',
        'views/domestico_product_assignment_views.xml',
        'views/res_partner_views.xml',
        'views/product_template_view.xml',
        'views/domestico_menus.xml',
    ]
}
