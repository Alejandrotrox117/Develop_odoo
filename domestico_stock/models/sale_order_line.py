from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    customer_id=fields.Many2one('res.partner',string="Proveedores",related="product_id.customer_id",store="True")
    