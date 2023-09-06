# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    _sql_constraints = [
        ('ci_uniq', 'unique(ci)', 'El número de la cédula ya se ha registrado anteriormente'),
        ('vat_uniq', 'unique(vat)', 'El número del RIF ya se ha registrado anteriormente'),
        ('phone_uniq', 'unique(phone)', 'El número de télefono ya se ha registrado anteriormente'),
        ('mobile_uniq', 'unique(mobile)', 'El número de télefono fijo ya se ha registrado anteriormente'),
    ]
    
    client_type_id = fields.Many2one('client.type', string='Rango de cliente')

    user_account = fields.Many2one('res.users', string="Perfil de usuario")
    ci = fields.Char('Cédula')
    gps = fields.Char('Dirección GPS')

    names = fields.Char('Nombres', compute='_compute_format_names_surnames', inverse='_inverse_names_surnames_to_name')
    surnames = fields.Char('Apellidos', compute='_compute_format_names_surnames', inverse='_inverse_names_surnames_to_name')

    country_id = fields.Many2one(default=lambda self: self._get_default_country_id())

    birthday = fields.Date(string='Fecha de nacimiento')
    
    pricelist_percent_ids = fields.One2many('res.partner.product.pricelist.percent', 'partner_id', string="Rangos")
    
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

    def form_user_account(self):
        return {
            'name': 'Perfil del usuario',
            'res_model': 'profile.user',
            'view_mode': 'form',
            'context': {
                'default_partner_id': self.id,
                'default_user_type': self.user_account.user_type if self.user_account else 'user',
            },
            'target': 'new',
            'type': 'ir.actions.act_window',
        }
    
    def form_user_password(self):
        return {
            'name': 'Cambiar contraseña',
            'res_model': 'change.password.wizard',
            'view_mode': 'form',
            'context': {
                'active_model': 'res.users',
                'active_ids': self.user_account.id,
            },
            'target': 'new',
            'type': 'ir.actions.act_window',
        }
    def _compute_display_name(self):
        for record in self:
            record.display_name = record.name if record.name else "Nuevo"

    def _get_default_country_id(self):
        return self.env['res.country'].search([('name', '=', 'Venezuela')])

    def _get_name(self):
        get_name = super(ResPartner, self)._get_name()

        total_name = get_name.split('\n', 1)
        
        name = self.name + '\n' + total_name[1] if len(total_name) > 1 else self.name

        return name
    
    @api.model
    def _commercial_fields(self):
        comercial_fields = super(ResPartner, self)._commercial_fields()
        comercial_fields.remove("vat")
        return comercial_fields

    def onchange_parent_id(self):
        if self.env.context.get('_partners_skip_fields_sync'):
            return
        
        return super(ResPartner, self).onchange_parent_id()