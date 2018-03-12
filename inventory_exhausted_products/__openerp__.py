# -*- coding: utf-8 -*-
# Copyright (c) 2017 QubiQ (http://www.qubiq.es)
#                    Xavier Jiménez <xavier.jimenez@qubiq.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Inventory Exhausted Products",
    "summary": "Add exhausted products on inventories",
    "version": "8.0.1.0.0",
    "category": "Inventory",
    "website": "https://www.qubiq.es/",
    "author": "QubiQ",
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
        "views/stock_inventory_view.xml",
    ],
}
