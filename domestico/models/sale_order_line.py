from odoo import models, fields

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _compute_price_unit(self):
        super(SaleOrderLine, self)._compute_price_unit()