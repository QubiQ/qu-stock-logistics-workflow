# -*- coding: utf-8 -*-
# Copyright 2018 Xavier Jiménez <xavier.jimenez@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Export Stock on Transfer',
    'version': '8.0.1.0.1',
    'summary': 'Export PrestaShop stock when transfering a picking',
    'category': 'Inventory',
    "website": "https://www.qubiq.es",
    "author": "QubiQ",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        'base',
        'stock',
        'product',
        'connector_prestashop',
    ],
    "data": [
    ],
}
