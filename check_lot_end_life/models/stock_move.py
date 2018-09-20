# Copyright 2018 Xavier Piernas <xavier.piernas@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    """
    Constrain to avoid saving lots whose end of life date is exceeded by its
    product life time
    """
    @api.multi
    @api.constrains('product_id', 'life_date')
    def _check_life_time(self):
        for sel in self.filtered(
            lambda x: x.product_id and x.product_id.life_time and
            x.life_date and datetime.today() + timedelta(
                days=x.product_id.life_time
            ) > fields.Datetime.from_string(x.life_date)
        ):
            raise UserError(
                _(
                    'The product exceeds the lot end of life date. '
                    'Limit date is ' + str(
                        datetime.today() + timedelta(
                            days=sel.product_id.life_time
                        )
                    ) + '.'
                )
            )
