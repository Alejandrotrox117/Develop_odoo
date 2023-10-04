from odoo import _, api, fields, models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_stock = fields.Float(string='Cantidad Restante', compute='_compute_product_stock')

    @api.depends('product_id')
    def _compute_product_stock(self):
        for record in self:
            order_product_count = sum(self.search([['product_id', '=', record.product_id.id]]).mapped('product_uom_qty'))
            record.product_stock = record.product_id.free_qty - order_product_count