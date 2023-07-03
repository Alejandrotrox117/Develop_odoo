# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    client_type_id = fields.Many2one('client.type', string='Tipo de cliente')

    user_account = fields.Many2one('res.users')
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

    def create_user_account(self):
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
            'new_passwd': 'Domestico.23'
        }

        self.env['change.password.user'].create(
            password_user).change_password_button()

        self.user_account = new_user.id

    def view_user_account(self):
        user_id = self.user_account.id
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'res.users',
            'view_mode': 'form',
            'res_id': user_id,
            'target': 'current',
            'view_id': self.env.ref('base.view_users_form').id
        }
        
    def _compute_display_name(self):
        for record in self:
            record.display_name = record.name if record.name else "Nuevo"
