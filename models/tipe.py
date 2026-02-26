# -*- coding: utf-8 -*-

from odoo import models, fields, api

class tipe(models.Model):
    _name = 'tipe.hotel'
    _description = 'this class contain master data for tipe/hotel room'
    _rec_name = 'nama_tipe'

    nama_tipe = fields.Char("Nama Tipe")
    harga = fields.Float("Harga")
