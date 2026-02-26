# -*- coding: utf-8 -*-
# from odoo import http


# class Hotelv18(http.Controller):
#     @http.route('/hotelv18/hotelv18', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hotelv18/hotelv18/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hotelv18.listing', {
#             'root': '/hotelv18/hotelv18',
#             'objects': http.request.env['hotelv18.hotelv18'].search([]),
#         })

#     @http.route('/hotelv18/hotelv18/objects/<model("hotelv18.hotelv18"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hotelv18.object', {
#             'object': obj
#         })

