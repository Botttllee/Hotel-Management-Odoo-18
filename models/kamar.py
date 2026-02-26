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
    default="available",
    )
    tipe_kamar = fields.Many2one("tipe.hotel", "Tipe Kamar")
    nomor_kamar = fields.Integer("No Kamar")
    booking_ids = fields.One2many("booking.hotel", "kamar_booking_id", string="Daftar Booking")
    booking_history_ids = fields.One2many("booking.history.hotel", "kamar_id", string="History Booking")
    current_guest = fields.Char("Guest Aktif", compute="_compute_current_guest")

    @api.depends("tipe_kamar", "nomor_kamar")
    def _compute_nama_kamar(self):
        for rec in self:
            if rec.tipe_kamar and rec.nomor_kamar:
                rec.nama_kamar = f"{rec.tipe_kamar.nama_tipe} {rec.nomor_kamar}"
            else:
                rec.nama_kamar = ""

    @api.depends("booking_ids.state", "booking_ids.nama_guest", "booking_ids.check_in")
    def _compute_current_guest(self):
        for rec in self:
            active_booking = rec.booking_ids.filtered(lambda x: x.state in ("confirmed", "checked_in"))
            active_booking = active_booking.sorted(key=lambda x: x.check_in or fields.Datetime.now())
            rec.current_guest = active_booking[0].nama_guest if active_booking else False
