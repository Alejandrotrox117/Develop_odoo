# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    ci = fields.Char('Cédula') 
    gps = fields.Char('Dirección GPS') 
