from odoo import api, fields, models


class AccountPaymentRegister(models.TransientModel):
    _name = 'account.payment.user.register'

    partner_id = fields.Many2one('res.partner', default=lambda self: self.env.user.partner_id.id)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company.id)

    bank_id = fields.Many2one('res.bank', related="journal_id.bank_id")
    is_internacional_bank = fields.Boolean(default=True, compute="_compute_is_internacional_bank")

    journal_id = fields.Many2one('account.journal', string="Cuenta")
    available_payment_method_line_ids = fields.Many2many('account.payment.method.line', 
                                             compute="_compute_available_payment_method_line_ids")
    payment_method_line_id = fields.Many2one('account.payment.method.line', string="Métodos de pago")

    file_ref = fields.Binary()
    filename = fields.Char(string='Comprobante')
    reference = fields.Char("Referencia")

    amount = fields.Monetary(string="Monto", currency_field="currency_id")
    currency_id = fields.Many2one('res.currency', compute="_compute_currency_id")

    date = fields.Date(string="Fecha")

    @api.depends('bank_id')
    def _compute_currency_id(self):
        for record in self:
            record.currency_id = record.bank_id.currency_id.id

    @api.depends('bank_id')
    def _compute_journal_id(self):
        for record in self:
            journal = self.env['account.journal'].search([('bank_account_id.bank_id', '=', record.bank_id.id)])
            record.journal_id = journal.id
    
    @api.depends('bank_id')
    def _compute_is_internacional_bank(self):
        for record in self:
            if record.bank_id:
                usd_id = self.env['res.currency'].search([('name', '=', 'USD')])

                record.is_internacional_bank = record.currency_id.id == usd_id.id

    @api.depends('journal_id')
    def _compute_available_payment_method_line_ids(self):
       for pay in self:
            pay.available_payment_method_line_ids = pay.journal_id._get_available_payment_method_lines('inbound')

    def action_create_payments(self):
        payment = {
            'partner_id': self.partner_id.id,
            'bank_id': self.bank_id.id,
            'journal_id': self.journal_id.id,
            'payment_method_line_id': self.payment_method_line_id.id,
            'amount': self.amount,
            'currency_id': self.currency_id.id,
            'date': self.date.strftime("%Y-%m-%d"),
            'reference': self.reference,
            'file_ref': self.file_ref,
            'filename': self.filename
        }

        create = self.env['account.payment'].sudo().create(payment)

        if create:
            
            return {
            'name': 'Solicitudes',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'tree,form'
        }