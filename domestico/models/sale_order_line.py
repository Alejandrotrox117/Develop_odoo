from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    pricelist_id = fields.Many2one('product.pricelist', related="order_id.pricelist_id")
    client_percent_id = fields.Many2one('product.pricelist.percent', compute="_compute_client_percent")

    @api.depends('order_id.partner_id', 'order_id.pricelist_id')
    def _compute_client_percent(self):
        for record in self:
            client_type = record.order_partner_id.client_type_id
            percent = record.pricelist_id.product_percent_id.filtered(lambda percent: percent.client_type_id.id == client_type.id)
            record.client_percent_id = percent

    def _compute_price_unit(self):
        for record in self:
            price = record.pricelist_item_id._get_price_percent(record.client_percent_id)
            if price:
                record.price_unit = price