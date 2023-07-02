# -*- coding: utf-8 -*-
{
    'name': "domestico",
    'author': "My Company",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'contacts', 'product', 'sale_management', 'hide_inbox_chatter', 'web_no_auto_save'],
    'data': [
        'security/domestico_groups.xml',
        'security/ir.model.access.csv',

        'views/res_partner_views.xml',
        'views/domestico_product_assignment_views.xml',
        'views/client_type_views.xml',
        'views/product_pricelist_views.xml',
        'views/domestico_menus.xml',
        'views/hide_menus.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            #Load theme before default primary variables 
            ('before', 'web/static/src/scss/primary_variables.scss', 'domestico/static/src/scss/domestico_theme.scss'),
        ]
    }
}
