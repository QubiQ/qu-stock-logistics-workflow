# Copyright 2019 Xavier Piernas <xavier.piernas@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, _


class ProductPriceHistory(models.Model):
    _inherit = 'product.price.history'

    previous_cost = fields.Float(
        string=_('Previous Cost'),
        default=0.0
    )

    @api.model
    def create(self, vals):
        product_id = self.env['product.product'].browse(vals['product_id'])
        if product_id.standard_price != product_id.previous_cost:
            if product_id:
                vals['previous_cost'] = product_id.previous_cost
            return super(ProductPriceHistory, self).create(vals)
