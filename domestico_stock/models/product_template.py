# -*- coding: utf-8 -*-

from odoo import models, fields,api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    taxes_id = fields.Many2many(default=[])
    cubicaje=fields.Float(string="Cubicaje (mts)")
    customer_id = fields.Many2one('res.partner', string="Proveedor")

class ProductProduct(models.Model):
    _inherit = 'product.product'
    cubicaje=fields.Float(string="Cubicaje (mts)")
    customer_id = fields.Many2one('res.partner',related="product_tmpl_id.customer_id" ,string="Proveedor")
    
    invoiced_qty = fields.Float(string='Invoiced Quantity', compute='_compute_invoiced_qty')

    def _compute_invoiced_qty(self):
        for product in self:
            invoices = self.env['account.move.line'].search([
                ('product_id', '=', product.id),
                ('move_id.state', '=', 'posted'),
                ('move_id.move_type', '=', 'out_invoice')
            ])
            invoiced_qty = sum(invoices.mapped('quantity'))
            product.invoiced_qty = invoiced_qty

    def _inverse_invoiced_qty(self):
        for product in self:
            invoices = self.env['account.move.line'].search([
                ('product_id', '=', product.id),
                ('move_id.state', '=', 'posted'),
                ('move_id.move_type', '=', 'out_invoice')
            ])
            invoiced_qty = sum(invoices.mapped('quantity'))
            product.invoiced_qty = invoiced_qty

    def _search_invoiced_qty(self, operator, value):
        invoices = self.env['account.move.line'].search([
            ('move_id.state', '=', 'posted'),
            ('move_id.move_type', '=', 'out_invoice')
        ])
        product_ids = invoices.mapped('product_id.id')
        return [('id', 'in', product_ids)]
    

    disponible = fields.Float(string='Disponible', compute='_compute_disponible')

    @api.depends('qty_available', 'invoiced_qty')
    def _compute_disponible(self):
        for product in self:
            disponible = product.qty_available - product.invoiced_qty
            product.disponible = disponible