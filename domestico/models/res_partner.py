# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    ci = fields.Char('Cédula') 
    gps = fields.Char('Dirección GPS') 

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

        self.env['change.password.user'].create(password_user).change_password_button()

        print("new user created")
