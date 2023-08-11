from odoo import models, fields, api

class ProfileUser(models.TransientModel):
    _name = "profile.user"
    _description = "Profile User"

    partner_id = fields.Many2one('res.partner', string='Contacto')
    
    user_id = fields.Many2one('res.users', string='Usuario', related='partner_id.user_account')

    groups_id = fields.Many2many('res.users.groups', string='Grupos', 
                            default=lambda self: self._get_users_groups())

    user_type = fields.Selection(string="Tipo de usuario", required=True,
                                selection=lambda self: self.env["res.users"].get_user_type)

    def _get_user_id(self):
        return self.env['res.partner'].browse(self._context.get("default_partner_id")).user_account

    def _get_users_groups(self):
        user = self._get_user_id()
        groups = user.groups_id.mapped('id') 
        return self.env['res.users.groups'].search([('group_id', 'in', groups)])

    @api.model
    def default_get(self, fields_list):
        fields_list.append("partner_id")
        res = super(ProfileUser, self).default_get(fields_list)
        return res

    def _get_groups_user_type(self):
        if self.user_type == "internal":
            group_id = [group.id for group in self.groups_id.mapped('group_id')]
        
        else:
            group_id = [self.env['ir.model.data'].sudo()\
                ._xmlid_to_res_id('domestico.domestico_group_' + self.user_type, raise_if_not_found=False)]

        return group_id

    def action_user_account(self):
        group_id = self._get_groups_user_type()

        if not self.partner_id.user_account:
            user = {
                'partner_id': self.partner_id.id,
                'login': self.partner_id.email,
                'company_id': self.env.company.id,
                "user_type": self.user_type,
                'groups_id': group_id,
            }

            new_user = self.env['res.users'].sudo().create(user)
            
            self.partner_id.sudo().write({'user_account': new_user.id})
        else:
            user = {
                "user_type": self.user_type,
                "groups_id": [(6, 0, group_id)],
            }

            self.user_id.sudo().write(user)

        return {'type': 'ir.actions.act_window_close'}

        