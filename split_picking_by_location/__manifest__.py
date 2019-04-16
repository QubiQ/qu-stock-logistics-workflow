# Copyright 2019 Xavier Piernas <xavier.piernas@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Split Picking By Location",
    "summary": "Split pickings depending on its destination location",
    "version": "11.0.1.0.0",
    "category": "Stock",
    "website": "https://www.qubiq.es",
    "author": "QubiQ, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "stock"
    ],
    "data": [
        "views/stock_picking.xml"
    ],
}
