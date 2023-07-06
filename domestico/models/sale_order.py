from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    partner_id = fields.Many2one(default=lambda self: self.env.user.partner_id)

    # warehouse_id = fields.Many2one(related="pricelist_id.warehouse_id")

    def _compute_pricelist_id(self):
        super(SaleOrder, self)._compute_pricelist_id()
        for order in self:
            if not order.pricelist_id: continue

            pricelist = self.env['product.pricelist'].search([('is_pricelist_active', '=', True)])
            order.pricelist_id = pricelist.id 
    
    @api.depends('pricelist_id')
    def _compute_warehouse_id(self):
        for order in self:
            if not order.pricelist_id and order.pricelist_id.warehouse_id: 
                super(SaleOrder, self)._compute_warehouse_id()
                continue

            order.warehouse_id = order.pricelist_id.warehouse_id.id

    def action_quotation_send(self):
        self.write({'state': 'sent'})
