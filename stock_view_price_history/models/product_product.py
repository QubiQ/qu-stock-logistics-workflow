# Copyright 2019 Xavier Piernas <xavier.piernas@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, _


class ProductProduct(models.Model):
    _inherit = 'product.product'

    previous_cost = fields.Float(
        string=_('Previous Cost'),
        default=0.0
    )

    @api.multi
    def write(self, vals):
        if 'standard_price' in vals:
            vals['previous_cost'] = self.standard_price
        return super(ProductProduct, self).write(vals)
