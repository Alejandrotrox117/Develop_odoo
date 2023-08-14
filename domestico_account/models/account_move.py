from odoo import api, fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'

    pricelist_id = fields.Many2one('product.pricelist', string='Ciclo',
                                default=lambda self: self._get_pricelist_id())

    def _get_pricelist_id(self):
        pricelist = self.env['product.pricelist'].search([('is_pricelist_active', '=', True)])
        return pricelist.id

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"
    
    pricelist_id = fields.Many2one('product.pricelist', related="move_id.pricelist_id")
    client_percent_id = fields.Many2one('product.pricelist.percent', compute="_compute_client_percent")

    pricelist_item_id = fields.Many2one('product.pricelist.item', compute='_compute_pricelist_item_id')

    def _compute_partner_id(self):
        for line in self:
            line.partner_id = line.move_id.partner_id
    @api.depends('product_id')
    def _compute_pricelist_item_id(self):
        for line in self:
            if not line.product_id or not line.pricelist_id:
                line.pricelist_item_id = False
            else:
                line.pricelist_item_id = line.pricelist_id._get_product_rule(line.product_id, 1.0)
    @api.depends('move_id.partner_id', 'pricelist_id')
    def _compute_client_percent(self):
        for line in self:
            client_type = line.partner_id.client_type_id
            percent = line.pricelist_id.product_percent_id.filtered(lambda percent: percent.client_type_id.id == client_type.id)
            line.client_percent_id = percent

    @api.depends('product_id', 'product_uom_id', 'pricelist_id')
    def _compute_price_unit(self):
        super(AccountMoveLine, self)._compute_price_unit()
        for line in self:
            price = line.pricelist_item_id._get_price_percent(line.client_percent_id)
            if price:
                line.price_unit = price