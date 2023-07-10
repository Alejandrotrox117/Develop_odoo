from odoo import api, fields, models
from odoo.exceptions import ValidationError

from datetime import datetime

class AccountPayment(models.Model):
    _inherit = 'account.payment'
    
    bank_id = fields.Many2one('res.bank', string="Banco")
    is_internacional_bank = fields.Boolean(store=True, compute="_compute_is_internacional_bank")

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
            if record.bank_id:
                record.currency_id = record.bank_id.currency_id
            else:
                super(AccountPayment, self)._compute_currency_id()
                
    @api.depends('currency_id')
    def _compute_is_internacional_bank(self):
        for record in self:
            if record.bank_id:
                usd_id = self.env['res.currency'].search([('name', '=', 'VES')])

                record.is_internacional_bank = record.currency_id.id != usd_id.id

    @api.constrains('bank_id', 'journal_id')
    def _constrain_currency_bank(self):
        for record in self:
            if record.bank_id.currency_id.id != record.journal_id.currency_id.id:
                raise ValidationError('La transacción no puede ser realizada debido a que las moneda de los bancos no coinciden.')

    def _valid_user_match(self):
        is_valid = self.create_uid.id != self.env.user.id

        return is_valid
    #CRUD Functions
    @api.model
    def create(self, vals_list):
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
        
        return super(AccountPayment, self).create(vals_list)