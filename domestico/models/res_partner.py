# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

class ResPartner(models.Model):
    _inherit = 'res.partner'

    ci = fields.Char('Cédula')
    gps = fields.Char('Dirección GPS')

    user = fields.One2many('res.users', 'partner_id')

    type_partner = fields.Selection(selection=[('contact', 'Contact'), ('user', 'Usuario')], default='contact')
    state = fields.Selection(selection=[('rejected', 'Rechazado'), ('refer', 'Referido'), ('user', 'Usuario')], string="Statu")

    refer_id = fields.Integer(inverse="_inverse_refer_id")

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
    
    def _inverse_refer_id(self):
        for record in self:
            record.parent_id = self.env['res.users'].browse(record.refer_id).partner_id.id or False

    @api.model
    def search(self, domain=[], **kwarg):
        # if self.env.context.get('params'):
        #     if self.env.context.get('params')['menu_id'] == self.env['ir.model.data']._xmlid_to_res_id('domestico.domestico_menu_root', raise_if_not_found=False):
        #         if self.env.user.has_group('domestico.domestico_group_user') and not self.env.user.has_group('domestico.domestico_group_manager'):
        #             domain = [('refer_id', '=', self.env.user.id)] + (domain or [])
        return super(ResPartner, self).search(domain, **kwarg)