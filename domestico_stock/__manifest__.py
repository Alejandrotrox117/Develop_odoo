# -*- coding: utf-8 -*-
{
    'name': "domestico stock",
    'author': "My Company",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['stock', 'domestico'],
    'data': [
        'security/domestico_stock_rules.xml',
        'security/ir.model.access.csv',

        'views/product_template_view.xml',
        'views/product_product_view.xml',
        'views/product_pricelist_views.xml',
        'views/stock_picking_views.xml',
        'views/domestico_proveedores.xml',
        'views/domestico_stock_menus.xml',
        
        
        'reports/returns_report.xml'
    ]
}
