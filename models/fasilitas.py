# -*- coding: utf-8 -*-

from odoo import models, fields, api

class fasilitas(models.Model):
    _name = 'fasilitas.hotel'
    _description = 'This Class Contain Facility For Hotel'
    _rec_name = 'nama_fasilitas'

    nama_fasilitas = fields.Char(string="Nama Kamar")
