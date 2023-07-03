from odoo import models, fields

class ResPartnerBanks(models.Model):
    _inherit = 'res.partner.bank'
    
    partner_id = fields.Many2one('res.partner','Cliente')
    
    ci = fields.Char("Cédula",related="partner_id.ci")

class ResBank(models.Model):
    _inherit = "res.bank"

    currency_id = fields.Many2one('res.currency', string="Moneda", required="1")