from odoo import api, fields, models

class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    bank_id = fields.Many2one('res.bank', string="Banco")
    is_internacional_bank = fields.Boolean(default=True, compute="_compute_is_internacional_bank")

    file_ref = fields.Binary()
    filename = fields.Char(string='Comprobante')
    reference = fields.Char("Referencia")

    def _init_payments(self, to_process, edit_mode=False):
        for payment in to_process:
            payment['create_vals'].update({
                'reference': self.reference,
                'bank_id': self.bank_id.id,
                'filename': self.filename,
                'file_ref': self.file_ref
            })
        return super(AccountPaymentRegister, self)._init_payments(to_process, edit_mode)
    
    @api.depends('bank_id')
    def _compute_currency_id(self):
        for record in self:
            if record.bank_id:
                record.currency_id = record.bank_id.currency_id
            else:
                super(AccountPaymentRegister, self)._compute_currency_id()
                
    @api.depends('bank_id')
    def _compute_is_internacional_bank(self):
        for record in self:
            if record.bank_id:
                usd_id = self.env['res.currency'].search([('name', '=', 'USD')])

                record.is_internacional_bank = record.currency_id.id == usd_id.id

    @api.model
    def default_get(self, fields_list): pass    