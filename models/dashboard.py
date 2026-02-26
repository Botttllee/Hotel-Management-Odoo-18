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

    @api.model
    def _get_metrics(self):
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

        return {
            "total_kamar": total_kamar,
            "available_kamar": available_kamar,
            "booking_kamar": booking_kamar,
            "booked_kamar": booked_kamar,
            "maintenance_kamar": maintenance_kamar,
            "occupancy_rate": ((booking_kamar + booked_kamar) / total_kamar * 100.0) if total_kamar else 0.0,
            "total_booking": booking_env.search_count([]),
            "draft_booking": booking_env.search_count([("state", "=", "draft")]),
            "confirmed_booking": booking_env.search_count([("state", "=", "confirmed")]),
            "checked_in_booking": booking_env.search_count([("state", "=", "checked_in")]),
            "done_booking": booking_env.search_count([("state", "=", "done")]),
            "cancelled_booking": booking_env.search_count([("state", "=", "cancelled")]),
            "today_checkin": booking_env.search_count(
                [("check_in", ">=", start_today), ("check_in", "<=", end_today)]
            ),
            "today_checkout": booking_env.search_count(
                [("check_out", ">=", start_today), ("check_out", "<=", end_today)]
            ),
        }

    @api.model
    def get_dashboard_metrics(self):
        return self._get_metrics()

    @api.depends()
    def _compute_dashboard(self):
        metrics = self._get_metrics()
        for rec in self:
            rec.total_kamar = metrics["total_kamar"]
            rec.available_kamar = metrics["available_kamar"]
            rec.booking_kamar = metrics["booking_kamar"]
            rec.booked_kamar = metrics["booked_kamar"]
            rec.maintenance_kamar = metrics["maintenance_kamar"]
            rec.occupancy_rate = metrics["occupancy_rate"]
            rec.total_booking = metrics["total_booking"]
            rec.draft_booking = metrics["draft_booking"]
            rec.confirmed_booking = metrics["confirmed_booking"]
            rec.checked_in_booking = metrics["checked_in_booking"]
            rec.done_booking = metrics["done_booking"]
            rec.cancelled_booking = metrics["cancelled_booking"]
            rec.today_checkin = metrics["today_checkin"]
            rec.today_checkout = metrics["today_checkout"]
