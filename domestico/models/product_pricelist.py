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

    is_pricelist_active = fields.Boolean('Ciclo Activo')

    product_percent_id = fields.One2many('product.pricelist.percent', 'pricelist_id')

    @api.onchange('is_pricelist_active')
    def _onchange_is_pricelist_active(self):
        if self.is_pricelist_active:
            for pricelist in self.search([('is_pricelist_active', '=', True)]):
                pricelist.write({'is_pricelist_active': False})
    

class ProductPricelist(models.Model):
    _inherit = "product.pricelist.item"

    price_private = fields.Float(string="Precio Privado")
    price_offert = fields.Float(string="Oferta PVP")

    def _get_price_percent(self, client_percent: ProductPricelistPercent):
        percents = self.pricelist_id.product_percent_id.filtered(lambda percent: percent.secuence <= client_percent.secuence)
        total_percent = sum(percents.mapped("percent")) / 100
        dif = self.price_offert - self.price_private
        price = self.price_offert - (dif * total_percent)
        return price
