# -*- coding: utf-8 -*-
# from odoo import http


# class Domestico(http.Controller):
#     @http.route('/domestico/domestico', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/domestico/domestico/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('domestico.listing', {
#             'root': '/domestico/domestico',
#             'objects': http.request.env['domestico.domestico'].search([]),
#         })

#     @http.route('/domestico/domestico/objects/<model("domestico.domestico"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('domestico.object', {
#             'object': obj
#         })
