# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    ci = fields.Char('Cédula')
    gps = fields.Char('Dirección GPS')
    
    user = fields.One2many('res.users', 'partner_id')
    user_count = fields.Integer(compute='_compute_user_count')

    type_partner = fields.Selection(selection=[('contact', 'Contact'), ('user', 'Usuario')], default='contact')
    state = fields.Selection(selection=[('rejected', 'Rechazado'), ('refer', 'Referido'), ('user', 'Usuario')], string="Statu")

    refer_id = fields.Integer(inverse="_inverse_refer_id")

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

    def create_user(self):
        group_id = self.env['ir.model.data']._xmlid_to_res_id('domestico.domestico_group_user', raise_if_not_found=False)

        user = {
            'partner_id': self.id,
            'login': self.email,
            'company_id': self.env.company.id,
            'groups_id': [group_id]
        }
        new_user = self.env['res.users'].create(user)

        psswd_wizard = self.env['change.password.wizard'].create({})

        password_user = {
            'wizard_id': psswd_wizard.id,
            'user_login': new_user.login,
            'user_id': new_user.id,
            'new_passwd': '12345'
        }

        self.env['change.password.user'].create(
            password_user).change_password_button()

        self.state = 'user'
    
    def rejected_partner(self):
        self.active = False
        self.state = 'rejected'

    def _compute_user_count(self):
        for record in self:
            record.user_count = len(record.user)
    
    def _inverse_refer_id(self):
        for record in self:
            record.parent_id = self.env['res.users'].browse(record.refer_id).partner_id.id or False