# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    ci = fields.Char('Cédula') 
    gps = fields.Char('Dirección GPS') 

    names = fields.Char('Nombres', 
                        compute='_compute_format_names_surnames', inverse='_inverse_names_surnames_to_name')
    surnames = fields.Char('Apellidos', 
                           compute='_compute_format_names_surnames', inverse='_inverse_names_surnames_to_name')

    @api.depends('name')
    def _compute_format_names_surnames(self):
        for record in self:
            split_names = record.name.split()
            length = len(split_names)

            if not length > 1:
                record.names = ""
                record.surnames = ""
                continue
            
            divided_length = length // 2

            record.names = " ".join(split_names[:divided_length])
            record.surnames = " ".join(split_names[divided_length:])

    def _inverse_names_surnames_to_name(self):
        for record in self:
            record.name = record.names + " " + record.surnames

