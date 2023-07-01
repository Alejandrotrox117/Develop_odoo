# -*- coding: utf-8 -*-
{
    'name': "domestico",
    'author': "My Company",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'stock', 'account', 'contacts', 'sale', 'hide_inbox_chatter', 'web_no_auto_save'],
    'data': [
        'security/domestico_groups.xml',
        'security/ir.model.access.csv',

        'views/res_partner_views.xml',
        'views/product_template_view.xml',
        'views/product_product_view.xml',
        'views/account_payment_view.xml',
        'views/domestico_product_assignment_views.xml',
        'views/client_type_views.xml',
        'views/product_pricelist_views.xml',
        'views/domestico_menus.xml',
        'views/views_menus_items.xml',
        'views/res_partner_bank_views.xml',        

        'wizard/account_payment_register_view.xml',
        'reports/invoice_report.xml'
    ],
    
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml'
    ],
    'assets': {
        'web._assets_primary_variables': [
            #Load theme before default primary variables 
            ('before', 'web/static/src/scss/primary_variables.scss', 'domestico/static/src/scss/domestico_theme.scss'),
        ]
    },
    'post_init_hook': 'create_update_bcv_job'
}
