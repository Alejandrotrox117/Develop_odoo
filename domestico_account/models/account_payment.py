from odoo import api, fields, models
from odoo.exceptions import ValidationError, Warning

from datetime import datetime

class AccountPayment(models.Model):
    _inherit = 'account.payment'
    
    bank_id = fields.Many2one('res.bank', string="Banco")
    is_internacional_bank = fields.Boolean(store=True, compute="_compute_is_internacional_bank")

    partner_id = fields.Many2one(default=lambda self: self.env.user.partner_id)

    file_ref = fields.Binary()
    filename = fields.Char(string='Comprobante')

    reference = fields.Char(string="Referencia")

    create_by = fields.Many2one('res.users', default=lambda self: self.env.user.id)

    bank_acc_number = fields.Char(string="Número de cuenta", compute='_compute_bank_acc_number', inverse='_inverse_bank_acc_number')
    
    journal_type = fields.Char(compute='_compute_journal_type')

    _sql_constraints = [
        ('reference_uniq', 'unique(reference)', 'La referencia ya se ha registrado anteriormente')
    ]
    
    ##### ONCHANGES #####
    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        partner_last_payment = self.search([('partner_id', '=', self.partner_id.id)], 
                                           order='date desc', limit=1)

        if partner_last_payment:
            self.bank_id = partner_last_payment.bank_id 

    ##### COMPUTES #####

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

    @api.depends('amount')
    def _compute_amount_company_currency_signed(self):
        for record in self:
            from_amount = record.amount
            to_currency = self.env.company.currency_id
            company = record.company_id
            date = record.date

            amount = record.currency_id._convert(from_amount, to_currency, company, date)
            record.amount_company_currency_signed = amount

    @api.depends('journal_id')
    def _compute_bank_acc_number(self):
        for record in self:
            if record.journal_id:
                record.bank_acc_number = record.journal_id.bank_account_id.acc_number

    @api.depends('journal_id')
    def _compute_journal_type(self):
        for record in self:
            record.journal_type = record.journal_id.type

    ##### INVERSE ######
    def _inverse_bank_acc_number(self):
        for record in self:
            if record.bank_acc_number:
                record.journal_id = self._get_journal_acc_numbe(record.bank_acc_number)

    #### CONSTRAINTS ####
    @api.constrains('bank_id', 'journal_id')
    def _constrain_currency_bank(self):
        for record in self:
            if record.bank_id.currency_id.id != record.journal_id.currency_id.id and record.journal_id.type == 'bank':
                raise ValidationError('La transacción no puede ser realizada debido a que las moneda de los bancos no coinciden.')

    # @api.constrains('partner_id')
    # def _constrain_partner_id(self):
    #     for record in self:
    #         have_account = self.env['account.move']\
    #                             .search([('partner_id', '=', record.partner_id.id), ('state', '!=', 'cancel'), ('payment_state', '!=', 'paid')])\
    #                             .exists()
    #         if not have_account:
    #             raise ValidationError('El cliente no tiene facturas registradas.')

    ##### CRUD Functions ######
    @api.model
    def create(self, vals_list):
        #si es importado
        if self.env.context.get('import_file'):
            payments = self.env['account.payment.method.line']
            payment_name = payments.browse(vals_list['payment_method_line_id']).name
            journal_id = self._get_journal_acc_numbe(vals_list['bank_acc_number'])
            payment_method = payments.search([('name', '=', payment_name), ('journal_id', '=', journal_id.id), ('payment_type', '=', 'inbound')])
            vals_list['payment_method_line_id'] = payment_method.id
            vals_list['journal_id'] = journal_id.id
            
            payment = super(AccountPayment, self).create(vals_list)

            if not 'partner_id' in vals_list:
                payment.partner_id = False

            return payment
        #validamos si el pago es de tipo efectivo
        if 'journal_id' in vals_list:
            if self.env['account.journal'].browse(vals_list['journal_id']).type == 'cash':
                return super(AccountPayment, self).create(vals_list)
        #validamos si el pago fue registrado previamente
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
        # if payment and payment.create_uid.id != self.env.user.id:
        if payment:
            payment.partner_id = vals_list['partner_id'] if 'partner_id' in vals_list else self.env.user.partner_id.id
            payment.action_post()
            return payment 
        else:
            raise ValidationError('El pago no ha sido registrado previamente por el personal autorizado por lo que no se puede validad.')

    ######## UTILS FUNCTIONS ########
    def _get_journal_acc_numbe(self, number):
        acc_number = self.env['res.partner.bank'].search([('acc_number', '=', number)])
        if not acc_number: 
            raise Warning('El número de cuenta no se encuentra registrado.')
        
        journal_id = self.env['account.journal'].search([('bank_account_id', '=', acc_number.id)])
        if not journal_id:
            raise Warning('El número de cuenta no se encuentra registrado.')
        
        return journal_id