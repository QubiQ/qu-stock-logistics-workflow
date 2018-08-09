# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# Copyright (c) 2018 QubiQ (http://www.qubiq.es)

{
    "name": "Stock valued picking",
    "version": "11.0.1.0.0",
    "author": "QubiQ, Odoo Community Association (OCA)",
    "website": "https://www.qubiq.es",
    "category": "stock",
    "license": "AGPL-3",
    "depends": [
        'sale',
        'stock',
        'sale_stock',
        'purchase',
        'purchase_discount'
    ],
    "data": [
        'reports/valued_picking.xml',
        'views/purchase_order.xml',
        'views/res_partner.xml',
        'views/stock_view.xml',
        'views/sale_order_view.xml'
    ],
    'installable': True,
    'application': False,
}
