# -*- coding: utf-8 -*-
# Copyright (c) 2017 QubiQ (http://www.qubiq.es)
#                    Xavier Jiménez <xavier.jimenez@qubiq.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Mass Cancel Procurement Orders",
    "summary": "Cancel multiple procurement orders at once",
    "version": "8.0.1.0.0",
    "category": "Warehouse",
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
        "procurement",
    ],
    "data": [
        "wizards/mass_cancel_procurement_order.xml",
    ],
}
