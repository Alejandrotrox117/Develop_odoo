from odoo import api, fields, models

class AccountPaymentMethodLine(models.Model):
    _inherit = 'account.payment.method.line'

    bank_id = fields.Many2one("res.bank", string="Banco", related="journal_id.bank_id")