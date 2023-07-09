# -*- coding: utf-8 -*-

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    taxes_id = fields.Many2many(default=[])
    cubicaje=fields.Float(string="Cubicaje (mts)")
    customer_id = fields.Many2one('res.partner', string="Proveedor")

class ProductProduct(models.Model):
    _inherit = 'product.product'
    cubicaje=fields.Float(string="Cubicaje (mts)")
    customer_id = fields.Many2one('res.partner', string="Proveedor")
