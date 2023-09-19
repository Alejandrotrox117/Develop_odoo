from odoo import _, api, fields, models

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    active = fields.Boolean(default=True)