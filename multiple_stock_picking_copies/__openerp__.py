# -*- coding: utf-8 -*-
# Copyright (c) 2017 QubiQ (http://www.qubiq.es)
#                    Xavier Jiménez <xavier.jimenez@qubiq.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Multiple Stock Picking Copies",
    "summary": "Print multiple stock picking copies",
    "version": "8.0.1.0.0",
    "category": "Stock",
    "website": "https://www.qubiq.es/",
    "author": "QubiQ, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "base",
        "stock",
    ],
    "data": [
        "views/stock_picking_view.xml",
    ],
}
