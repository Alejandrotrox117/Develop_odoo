from odoo import models, fields


class ResUsers(models.Model):
    _inherit = "res.users"

    @property
    def get_user_type(self):
        return [
            ('user', 'Cliente'),
            ('vendor', 'Proveedor'),
            ('internal', 'Interno'),
            ('manager', 'Administrador'),
        ]

    user_type = fields.Selection(string="Tipo de usuario", default="user",
                                selection=lambda self: self.get_user_type)


class ResUsersGroups(models.Model):
    _name = "res.users.groups"
    _description = "Res Users Groups"

    name = fields.Char(string="Módulo", required=True)
    group_id = fields.Many2one('res.groups', string="Grupo", required=True)
