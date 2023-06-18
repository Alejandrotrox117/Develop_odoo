# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    ci = fields.Char('Cédula') 
    gps = fields.Char('Dirección GPS')


class AccountPayment(models.Model):
    _inherit = 'account.payment'
    
    referencia = fields.Char(string="Referencia Bancaria")
    