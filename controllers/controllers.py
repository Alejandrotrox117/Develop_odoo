# -*- coding: utf-8 -*-
# from odoo import http


# class Directorio(http.Controller):
#     @http.route('/directorio/directorio', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/directorio/directorio/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('directorio.listing', {
#             'root': '/directorio/directorio',
#             'objects': http.request.env['directorio.directorio'].search([]),
#         })

#     @http.route('/directorio/directorio/objects/<model("directorio.directorio"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('directorio.object', {
#             'object': obj
#         })
