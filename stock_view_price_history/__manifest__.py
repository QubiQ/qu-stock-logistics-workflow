# Copyright 2019 Joan Segui <joan.segui@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Stock View Price History",
    "summary": "View with the changes of the price in a product",
    "version": "11.0.1.0.0",
    "category": "Stock",
    "website": "https://www.qubiq.es",
    "author": "QubiQ",
    "license": "AGPL-3",
    "depends": [
        "product",
        "purchase",
    ],
    "data": [
        "views/stock_history_cost_view.xml",
    ],
    "application": False,
    "installable": True,
}
