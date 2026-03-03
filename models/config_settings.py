# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    hotel_report_theme = fields.Selection(
        [("classic", "Classic Blue"), ("forest", "Forest Green"), ("sunset", "Sunset Orange")],
        string="Report Theme",
        default="classic",
        config_parameter="hotelv18.hotel_report_theme",
    )
    hotel_report_layout = fields.Selection(
        [("standard", "Standard"), ("compact", "Compact")],
        string="Hotel Report Layout",
        default="standard",
        config_parameter="hotelv18.hotel_report_layout",
    )
    hotel_report_show_guest_phone = fields.Boolean(
        string="Show Guest Phone in Report",
        default=True,
        config_parameter="hotelv18.hotel_report_show_guest_phone",
    )
    hotel_report_show_financial = fields.Boolean(
        string="Show Financial Summary",
        default=True,
        config_parameter="hotelv18.hotel_report_show_financial",
    )
    hotel_report_footer_note = fields.Char(
        string="Report Footer Note",
        config_parameter="hotelv18.hotel_report_footer_note",
    )
