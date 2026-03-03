# -*- coding: utf-8 -*-

from datetime import datetime, time

from odoo import api, fields, models
from odoo.tools import date_utils


class HotelMonthlyReportWizard(models.TransientModel):
    _name = "hotel.monthly.report.wizard"
    _description = "Wizard Monthly Hotel Report"

    date_start = fields.Date("Start Date", required=True, default=lambda self: date_utils.start_of(fields.Date.today(), "month"))
    date_end = fields.Date("End Date", required=True, default=lambda self: date_utils.end_of(fields.Date.today(), "month"))

    booking_ids = fields.Many2many("booking.hotel", string="Bookings", compute="_compute_summary")
    booking_count = fields.Integer("Total Booking", compute="_compute_summary")
    guest_count = fields.Integer("Total Guest", compute="_compute_summary")
    confirmed_count = fields.Integer("Confirmed", compute="_compute_summary")
    checked_in_count = fields.Integer("Checked In", compute="_compute_summary")
    done_count = fields.Integer("Done", compute="_compute_summary")
    cancelled_count = fields.Integer("Cancelled", compute="_compute_summary")
    gross_revenue = fields.Float("Gross Revenue", compute="_compute_summary")
    realized_revenue = fields.Float("Realized Revenue", compute="_compute_summary")

    @api.depends("date_start", "date_end")
    def _compute_summary(self):
        for rec in self:
            rec.booking_ids = False
            rec.booking_count = 0
            rec.guest_count = 0
            rec.confirmed_count = 0
            rec.checked_in_count = 0
            rec.done_count = 0
            rec.cancelled_count = 0
            rec.gross_revenue = 0.0
            rec.realized_revenue = 0.0

            if not rec.date_start or not rec.date_end or rec.date_end < rec.date_start:
                continue

            domain = [
                ("check_in", ">=", datetime.combine(rec.date_start, time.min)),
                ("check_in", "<=", datetime.combine(rec.date_end, time.max)),
            ]
            bookings = self.env["booking.hotel"].search(domain, order="check_in asc")
            rec.booking_ids = bookings
            rec.booking_count = len(bookings)
            rec.guest_count = len(set(filter(None, bookings.mapped("nama_guest"))))
            rec.confirmed_count = len(bookings.filtered(lambda b: b.state == "confirmed"))
            rec.checked_in_count = len(bookings.filtered(lambda b: b.state == "checked_in"))
            rec.done_count = len(bookings.filtered(lambda b: b.state == "done"))
            rec.cancelled_count = len(bookings.filtered(lambda b: b.state == "cancelled"))

            non_cancelled = bookings.filtered(lambda b: b.state != "cancelled")
            done_bookings = bookings.filtered(lambda b: b.state == "done")
            rec.gross_revenue = sum(non_cancelled.mapped("total_harga"))
            rec.realized_revenue = sum(done_bookings.mapped("total_harga"))

    def action_print_monthly_report(self):
        self.ensure_one()
        return self.env.ref("hotelv18.action_report_monthly_hotel_summary").report_action(self)
