from odoo import _, api, fields, models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_virtual_available = fields.Float(string='Disponible', compute='_compute_product_virtual_available')

    @api.depends('product_id')
    def _compute_product_virtual_available(self):
        for record in self:
            record.product_virtual_available = record.product_id.virtual_available