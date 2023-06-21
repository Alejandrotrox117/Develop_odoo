from odoo.exceptions import UserError
from odoo import models, fields, api

#Modelo de el formulario de pagos

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    referencia = fields.Char(string="Referencia de transferencia", required=True)

    _sql_constraints = [
        ("referencia_unique", "unique(referencia)", "La referencia de pago debe ser única"),
    ]
    
class AccountMove(models.Model):
    _inherit = 'account.move'
    
    referencia = fields.Char(string="Referencia de transferencia", readonly=True)

class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    referencia = fields.Char(string="Referencia de transferencia", required=True)