from odoo import api, fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'

    pricelist_id = fields.Many2one('product.pricelist', string='Ciclo',
                                default=lambda self: self._get_pricelist_id())

    amount_weekly = fields.Monetary(compute='_compute_amount_weekly', currency_field='currency_id')

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        res = super(AccountMove, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby, lazy=lazy)
        
        if 'amount_weekly' in fields:
            for line in res:
                if '__domain' in line:
                    lines = self.search(line['__domain'])
                    total_amount_weekly = 0.0
                    for record in lines:
                        total_amount_weekly += record.amount_weekly
                    line['amount_weekly'] = total_amount_weekly

        return res

    def _get_pricelist_id(self):
        pricelist = self.env['product.pricelist'].search([('is_pricelist_active', '=', True)])
        return pricelist.id

        
    def _compute_amount_weekly(self):
        for record in self:
            if record.amount_total_signed > 0:
                record.amount_weekly = record.amount_total_signed / 8
            else:
                record.amount_weekly = 0

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"
    
    pricelist_id = fields.Many2one('product.pricelist', related="move_id.pricelist_id")
    client_percent_id = fields.Many2one('product.pricelist.percent', compute="_compute_client_percent")

    pricelist_item_id = fields.Many2one('product.pricelist.item', compute='_compute_pricelist_item_id')

    product_percent = fields.Float(string='Descuento', compute='_compute_product_percent')
    price_percent = fields.Float(string='Oferta PVP', compute='_compute_price_percent')
    
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
            percent = self.env['res.partner.product.pricelist.percent'].search([('partner_id', '=', line.move_id.partner_id.id), ('pricelist_id', '=', line.pricelist_id.id)])
            line.client_percent_id = percent.pricelist_percent_id.id

    @api.depends('product_id', 'product_uom_id', 'pricelist_id')
    def _compute_product_percent(self):
        for line in self:
            price = line.pricelist_item_id._get_price_percent(line.client_percent_id)
            line.product_percent = price if price else 0

    @api.depends('product_id', 'pricelist_item_id')
    def _compute_price_percent(self):
        for line in self:
            line.price_percent = line.pricelist_item_id.fixed_price

    @api.depends('product_id', 'product_uom_id')
    def _compute_price_unit(self):
        super(AccountMoveLine, self)._compute_price_unit()
        for line in self:
            line.price_unit = line.price_percent - line.product_percent
