# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductAssignment(models.Model):
    _name = 'domestico.product.assignment'
    _description = 'Asignación de Productos'

    product_id = fields.Many2one('product.template', string='Producto')
    product_count = fields.Integer(string='Cantidad')