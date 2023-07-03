from odoo import api, fields, models

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    payments = fields.Selection(string="Método de pago", 
                                selection=[
                                        ('transfer', 'Transferencia',),
                                        ('p2p', 'Pago Movil'),
                                        ('sale_point', 'Punto de Venta')
                                    ]
                                )
    
    bank_id = fields.Many2one('res.bank', string="Banco")
    is_internacional_bank = fields.Boolean(default=True, compute="_compute_is_internacional_bank")
    
    file_ref = fields.Binary()
    filename = fields.Char(string='Comprobante')

    reference = fields.Char("Referencia")
    
    _sql_constraints = [
        ('reference_uniq', 'unique(reference)', 'La referencia debe ser unica')
    ]

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        partner_last_payment = self.search([('partner_id', '=', self.partner_id.id)], order='date desc', limit=1)

        if len(partner_last_payment) > 0 and not self.bank_id:
            self.bank_id = partner_last_payment.bank_id 

    @api.depends('bank_id')
    def _compute_currency_id(self):
        for record in self:
            if record.bank_id:
                record.currency_id = record.bank_id.currency_id
            else:
                super(AccountPayment, self)._compute_currency_id()
                
    @api.depends('bank_id')
    def _compute_is_internacional_bank(self):
        for record in self:
            if record.bank_id:
                usd_id = self.env['res.currency'].search([('name', '=', 'USD')])

                record.is_internacional_bank = record.currency_id.id == usd_id.id

