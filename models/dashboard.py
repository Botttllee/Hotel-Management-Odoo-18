# -*- coding: utf-8 -*-

from datetime import datetime, time

from odoo import api, fields, models


class hotelDashboard(models.Model):
    _name = "hotel.dashboard"
    _description = "Hotel Manager Dashboard"

    name = fields.Char("Nama Dashboard", default="Dashboard Manager", required=True)

    total_kamar = fields.Integer("Total Kamar", compute="_compute_dashboard")
    available_kamar = fields.Integer("Available", compute="_compute_dashboard")
    booking_kamar = fields.Integer("On Booking", compute="_compute_dashboard")
    booked_kamar = fields.Integer("Checked In", compute="_compute_dashboard")
    maintenance_kamar = fields.Integer("Maintenance", compute="_compute_dashboard")
    occupancy_rate = fields.Float("Occupancy (%)", compute="_compute_dashboard")

    total_booking = fields.Integer("Total Booking", compute="_compute_dashboard")
    draft_booking = fields.Integer("Draft Booking", compute="_compute_dashboard")
    confirmed_booking = fields.Integer("Confirmed", compute="_compute_dashboard")
    checked_in_booking = fields.Integer("Checked In", compute="_compute_dashboard")
    done_booking = fields.Integer("Done", compute="_compute_dashboard")
    cancelled_booking = fields.Integer("Cancelled", compute="_compute_dashboard")
    today_checkin = fields.Integer("Check In Hari Ini", compute="_compute_dashboard")
    today_checkout = fields.Integer("Check Out Hari Ini", compute="_compute_dashboard")

    @api.depends()
    def _compute_dashboard(self):
        kamar_env = self.env["kamar.hotel"]
        booking_env = self.env["booking.hotel"]

        total_kamar = kamar_env.search_count([])
        available_kamar = kamar_env.search_count([("status_kamar", "=", "available")])
        booking_kamar = kamar_env.search_count([("status_kamar", "=", "booking")])
        booked_kamar = kamar_env.search_count([("status_kamar", "=", "booked")])
        maintenance_kamar = kamar_env.search_count([("status_kamar", "=", "maintenance")])

        today = fields.Date.context_today(self)
        start_today = datetime.combine(today, time.min)
        end_today = datetime.combine(today, time.max)

        for rec in self:
            rec.total_kamar = total_kamar
            rec.available_kamar = available_kamar
            rec.booking_kamar = booking_kamar
            rec.booked_kamar = booked_kamar
            rec.maintenance_kamar = maintenance_kamar
            rec.occupancy_rate = ((booking_kamar + booked_kamar) / total_kamar * 100.0) if total_kamar else 0.0

            rec.total_booking = booking_env.search_count([])
            rec.draft_booking = booking_env.search_count([("state", "=", "draft")])
            rec.confirmed_booking = booking_env.search_count([("state", "=", "confirmed")])
            rec.checked_in_booking = booking_env.search_count([("state", "=", "checked_in")])
            rec.done_booking = booking_env.search_count([("state", "=", "done")])
            rec.cancelled_booking = booking_env.search_count([("state", "=", "cancelled")])
            rec.today_checkin = booking_env.search_count(
                [("check_in", ">=", start_today), ("check_in", "<=", end_today)]
            )
            rec.today_checkout = booking_env.search_count(
                [("check_out", ">=", start_today), ("check_out", "<=", end_today)]
            )
