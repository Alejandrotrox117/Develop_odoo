from odoo import models, fields, api

class ProductPricelistPercent(models.Model):
    _name = "product.pricelist.percent"
    _description = "Percent product pricelist"

    _order = "secuence desc"

    secuence = fields.Integer(string="Secuencia")

    client_type_id = fields.Many2one('client.type', string="Tipo de cliente")

    percent = fields.Float(string="Porcerntaje")

    pricelist_id = fields.Many2one('product.pricelist')



class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    product_percent_id = fields.One2many('product.pricelist.percent', 'pricelist_id')

    warehouse_id = fields.Many2one('stock.warehouse', string="Inventario de ciclo")
