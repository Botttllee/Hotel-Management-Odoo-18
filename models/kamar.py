# -*- coding: utf-8 -*-

from odoo import models, fields, api

class kamar(models.Model):
    _name = 'kamar.hotel'
    _description = 'this class contain master data for kamar/hotel room'
    _rec_name = 'nama_kamar'

    nama_kamar = fields.Char(
    string="Nama Kamar",
    compute="_compute_nama_kamar",
    store=True
    )

    status_kamar = fields.Selection(
    [
        ("available", "Available"),
        ("booking", "Booking"),
        ("booked", "Booked"),
        ("maintenance", "Maintenance"),
    ],
    string="Status Kamar",
    )
    tipe_kamar = fields.Many2one("tipe.hotel", "Tipe Kamar")
    nomor_kamar = fields.Integer("No Kamar")

    @api.depends("tipe_kamar", "nomor_kamar")
    def _compute_nama_kamar(self):
        for rec in self:
            if rec.tipe_kamar and rec.nomor_kamar:
                rec.nama_kamar = f"{rec.tipe_kamar.nama_tipe} {rec.nomor_kamar}"
            else:
                rec.nama_kamar = ""

