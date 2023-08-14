from odoo import models, fields, api

class ResPartnerBanks(models.Model):
    _inherit = 'res.partner.bank'
    
    partner_id = fields.Many2one('res.partner',string='Cliente')
    
    ci = fields.Char(string="Cédula",related="partner_id.ci")

    payment_ids = fields.Many2many('res.bank.payment', string='Metodos de Pago')


class ResBank(models.Model):
    _inherit = "res.bank"

    currency_id = fields.Many2one('res.currency', string="Moneda", required="1")

class ResBankPayment(models.Model):
    _name = "res.bank.payment"
    _description= "Res bank payment"

    name = fields.Char('Nombre')