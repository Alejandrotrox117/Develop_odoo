from odoo import api, fields, models

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    reference = fields.Char("Referencia")
    
    _sql_constraints = [
        ('reference_uniq', 'unique(reference)', 'La referencia debe ser unica')
    ]


