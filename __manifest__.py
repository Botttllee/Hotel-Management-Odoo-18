# -*- coding: utf-8 -*-
{
    'name': "hotelv18",
    'summary': "This Module Handle Basic Management For Hotel",
    'description': """
    This Module Handle Booking, Re-Schedule, Sending Email, Invoice, Reporting this module for odoo 18
    """,
    'author': "Hendrik",
    'website': "https://github.com/repos",
    'category': 'Hotel',
    'version': '18.0',
    'sequence': 1,
    'application': True,
    'auto_install': False,
    # any module necessary for this one to work correctly
    'depends': ['base', 'web'],
    'assets': {
        'web.assets_backend': [
            'hotelv18/static/src/scss/dashboard_visual.scss',
            'hotelv18/static/src/js/dashboard_visual.js',
            'hotelv18/static/src/xml/dashboard_visual.xml',
        ],
    },
    'data': [
        'security/ir.model.access.csv',
        'views/main.xml',
        'views/dashboard.xml',
        'views/dashboard_visual.xml',
        'views/kamar.xml',
        'views/tipe.xml',
        'views/booking.xml',
        'views/fasilitas.xml',
    ],
}
