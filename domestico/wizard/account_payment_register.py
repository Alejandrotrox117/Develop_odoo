from odoo import api, fields, models

class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    reference = fields.Char("Referencia")
    def _init_payments(self, to_process, edit_mode=False):
        for payment in to_process:
            payment['create_vals'].update({
                'reference': self.reference
            })
        return super(AccountPaymentRegister, self)._init_payments(to_process, edit_mode)