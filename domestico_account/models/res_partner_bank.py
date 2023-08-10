from odoo import models, fields, api

class ResPartnerBanks(models.Model):
    _inherit = 'res.partner.bank'
    
    partner_id = fields.Many2one('res.partner',string='Cliente')
    
    ci = fields.Char(string="Cédula",related="partner_id.ci")

    payment_ids = fields.Many2many('account.payment.method.line', string='Metodos de Pago')


class ResBank(models.Model):
    _inherit = "res.bank"

    currency_id = fields.Many2one('res.currency', string="Moneda", required="1")