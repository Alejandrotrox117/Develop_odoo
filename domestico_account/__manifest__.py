# -*- coding: utf-8 -*-
{
    'name': "domestico account",
    'author': "My Company",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['account', 'domestico'],
    'data': [
        'security/domestico_account_groups.xml',
        'security/ir.model.access.csv',

        'views/res_partner_bank_views.xml',        
        'views/account_payment_view.xml',
        'views/domestico_account_menus.xml',

        'reports/invoice_report.xml',
        'reports/sale_order_report.xml',    
        'wizard/account_payment_register_view.xml',
    ],
    'post_init_hook': 'create_update_bcv_job'
}
