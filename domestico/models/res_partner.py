# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    ci = fields.Char('Cédula') 
    gps = fields.Char('Dirección GPS')


#Modelo de pagos en el modulo de facturacion
class AccountPayment(models.Model):
    _inherit = 'account.payment'
    
    referencia = fields.Char(string="Referencia de transferencia",required=True)
    
# class AccountPaymentRegister(models.TransientModel):
#     _inherit = 'account.payment.register'

#     referencia = fields.Char(string='Referencia de transferencia')
   