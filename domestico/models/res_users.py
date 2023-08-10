from odoo import models, fields

class ResUsers(models.Model):
    _inherit = "res.users"

    user_type = fields.Selection(string="Tipo de usuario", default="user",
                                 selection=[
                                     ('user', 'Cliente'),
                                     ('vendor', 'Proveedor'),
                                     ('internal', 'Interno'),
                                     ('admin', 'Administrador'),
                                 ])

class ResUsersGroups(models.Model):
    _name = "res.users.groups"
    _description = "Res Users Groups"

    name = fields.Char(string="Módulo", required=True)
    group_id = fields.Many2one('res.groups', string="Grupo", required=True)
