# -*- coding: utf-8 -*-

from odoo import fields, models


class bookingHistory(models.Model):
    _name = "booking.history.hotel"
    _description = "History status booking per kamar"
    _order = "tanggal desc, id desc"

    booking_id = fields.Many2one("booking.hotel", string="Booking", required=True, ondelete="cascade")
    kamar_id = fields.Many2one("kamar.hotel", string="Kamar", required=True)
    nama_guest = fields.Char("Nama Guest", required=True)
    aksi = fields.Selection(
        [
            ("confirm", "Confirm Booking"),
            ("checkin", "Check In"),
            ("checkout", "Check Out"),
            ("cancel", "Cancel Booking"),
        ],
        string="Aksi",
        required=True,
    )
    tanggal = fields.Datetime("Tanggal", default=fields.Datetime.now, required=True)
