# Copyright 2019 Joan Segui <joan.segui@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models, _


class ProductPriceHistory(models.Model):
    _inherit = "product.price.history"

    actual_cost = fields.Float(
        string=_('Actual Cost'),
        related='product_id.standard_price',
        store=True,
        readonly=True
    )
    name_product = fields.Char(
        string=_('Product Name'),
        related='product_id.name',
        store=True,
        readonly=True
    )
