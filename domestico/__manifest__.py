# -*- coding: utf-8 -*-
{
    'name': "domestico",
    'author': "My Company",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base','product', 'account', 'contacts'],
    'data': [
        'security/domestico_groups.xml',
        # 'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'views/templates.xml',
        'views/product_template_view.xml',
    ]
}
