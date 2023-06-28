from odoo import api, models, fields

class DomesticoClientType(models.Model):
    _name = "client.type"
    _description = "Domestico client type"

    _order = "secuence desc"

    name = fields.Char(string='Nombre')

    secuence = fields.Integer(string="Secuencia")

