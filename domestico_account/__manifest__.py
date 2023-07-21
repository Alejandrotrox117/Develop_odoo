# -*- coding: utf-8 -*-
{
    'name': "domestico account",
    'author': "My Company",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['account', 'domestico'],
    'data': [
        'security/domestico_account_rules.xml',
        'security/ir.model.access.csv',

        'wizard/account_payment_user_register_view.xml',
        'wizard/account_payment_register_view.xml',

        'views/res_partner_bank_views.xml',        
        'views/account_payment_view.xml',
        'views/account_move_view.xml',
        'views/domestico_account_menus.xml',

        'reports/invoice_report.xml',
    ],
    'post_init_hook': 'create_update_bcv_job'
}
