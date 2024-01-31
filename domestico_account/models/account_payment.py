from odoo import api, fields, models
from odoo.exceptions import ValidationError

from datetime import datetime

class AccountPayment(models.Model):
    _inherit = 'account.payment'
    
    bank_id = fields.Many2one('res.bank', string="Banco")
    is_internacional_bank = fields.Boolean(store=True, compute="_compute_is_internacional_bank",
                                            inverse="_inverse_is_internacional_bank")

    partner_id = fields.Many2one(default=lambda self: self.env.user.partner_id)

    file_ref = fields.Binary()
    filename = fields.Char(string='Comprobante')

    reference = fields.Char(string="Referencia", required=True)

    create_by = fields.Many2one('res.users', default=lambda self: self.env.user.id)
    
    _sql_constraints = [
        ('reference_uniq', 'unique(reference)', 'La referencia ya se ha registrado anteriormente')
    ]

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        partner_last_payment = self.search([('partner_id', '=', self.partner_id.id)], 
                                           order='date desc', limit=1)

        if partner_last_payment:
            self.bank_id = partner_last_payment.bank_id 

    @api.depends('bank_id')
    def _compute_currency_id(self):
        for record in self:
            if record.is_internacional_bank:
                record.currency_id = self.env.ref('base.USD').id
            else: 
                record.currency_id = self.env.ref('base.VES').id
            # else:
            #     super(AccountPayment, self)._compute_currency_id()
                
    @api.depends('currency_id')
    def _compute_is_internacional_bank(self):
        for record in self:
            if record.bank_id:
                usd_id = self.env.ref('base.USD')

                record.is_internacional_bank = record.currency_id.id == usd_id.id

    def _inverse_is_internacional_bank(self):
        for record in self:
            if record.is_internacional_bank:
                record.currency_id = self.env.ref('base.USD').id
            else: 
                record.currency_id = self.env.ref('base.VES').id

    @api.constrains('bank_id', 'journal_id')
    def _constrain_currency_bank(self):
        for record in self:
            if record.bank_id.currency_id.id != record.journal_id.currency_id.id:
                raise ValidationError('La transacción no puede ser realizada debido a que las moneda de los bancos no coinciden.')

    def _valid_user_match(self):
        is_valid = self.create_uid.id != self.env.user.id

        return is_valid

    @api.constrains('partner_id')
    def _constrain_partner_id(self):
        for record in self:
            have_account = self.env['account.move']\
                                .search([('partner_id', '=', record.partner_id.id), ('state', '!=', 'cancel'), ('payment_state', '!=', 'paid')])\
                                .exists()
            if not have_account:
                raise ValidationError('El cliente no tiene facturas registradas.')
    #CRUD Functions
    @api.model
    def create(self, vals_list):
        if self.env.context.get('import_file'):
            payments = self.env['account.payment.method.line']
            payment_name = payments.browse(vals_list['payment_method_line_id']).name
            payment_method = payments.search([('name', '=', payment_name), ('journal_id', '=', vals_list['journal_id']), ('payment_type', '=', 'inbound')])
            vals_list['payment_method_line_id'] = payment_method.id
            return super(AccountPayment, self).create(vals_list)

        payment = self.search(
            [
                ('state', '=', 'draft'),
                ('reference', '=', vals_list['reference']),
                ('bank_id', '=', vals_list['bank_id']),
                ('amount', '=', vals_list['amount']),
                ('journal_id', '=', vals_list['journal_id']),
                ('payment_method_line_id', '=', vals_list['payment_method_line_id']),
                ('date', '=', datetime.strptime(vals_list['date'], "%Y-%m-%d")),
            ]
        )

        if payment and payment._valid_user_match():
            payment.action_post()
            return payment 
        else:
            raise ValidationError('El pago no ha sido registrado previamente por el personal autorizado por lo que no se puede validad.')