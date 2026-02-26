# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class booking(models.Model):
    _name = 'booking.hotel'
    _description = 'this class contain master data for booking/hotel room'
    _rec_name = 'sequence'

    # Basic Information
    sequence = fields.Char(
        string="Booking Number",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _("New"),
    )
    check_in = fields.Datetime("Check In")
    check_out = fields.Datetime("Check Out")
    nama_guest = fields.Char("Nama Guest")
    nomor_telp_guest = fields.Integer("No Tlp")

    status_booking_id = fields.Selection(related="kamar_booking_id.status_kamar", string="Status Booking")

    # Booking Information
    kamar_booking_id = fields.Many2one("kamar.hotel", "Kamar")
    harga_kamar_id = fields.Many2one("tipe.hotel", "Harga", readonly=True)
    hari = fields.Integer("Hari", default=1)
    total_harga = fields.Float("Total Harga", compute="_compute_total_harga", store=True)

    @api.onchange("kamar_booking_id")
    def _onchange_kamar_booking_id(self):
        for rec in self:
            rec.harga_kamar_id = rec.kamar_booking_id.tipe_kamar

    @api.onchange("check_in", "check_out")
    def _onchange_check_date(self):
        for rec in self:
            if rec.check_in and rec.check_out and rec.check_out > rec.check_in:
                duration = rec.check_out - rec.check_in
                rec.hari = max(duration.days, 1)
            elif rec.hari < 1:
                rec.hari = 1

    @api.depends("harga_kamar_id.harga", "hari")
    def _compute_total_harga(self):
        for rec in self:
            rec.total_harga = rec.harga_kamar_id.harga * max(rec.hari, 1)

    @api.constrains("hari")
    def _check_hari(self):
        for rec in self:
            if rec.hari < 1:
                raise ValidationError(_("Hari minimal 1."))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("sequence") or vals["sequence"] == _("New"):
                vals["sequence"] = self.env["ir.sequence"].next_by_code("booking.hotel") or _("New")

            if vals.get("kamar_booking_id") and not vals.get("harga_kamar_id"):
                kamar = self.env["kamar.hotel"].browse(vals["kamar_booking_id"])
                vals["harga_kamar_id"] = kamar.tipe_kamar.id

            vals["hari"] = max(vals.get("hari", 1), 1)

        return super().create(vals_list)

    def write(self, vals):
        if "kamar_booking_id" in vals and "harga_kamar_id" not in vals:
            kamar = self.env["kamar.hotel"].browse(vals["kamar_booking_id"])
            vals["harga_kamar_id"] = kamar.tipe_kamar.id

        if "hari" in vals:
            vals["hari"] = max(vals["hari"], 1)

        return super().write(vals)
