# Copyright 2018 Xavier Piernas <xavier.piernas@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.multi
    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        self.check_life_time()
        return res

    """
    Checks every move in the picking for products with a life time and raises
    an error if finds any lot whose end of life date is exceeded by its product
    life time
    """
    def check_life_time(self):
        exceed = {}
        for move in self.filtered(
            lambda x: x.picking_type_id.code == 'incoming'
        ).mapped('move_lines').filtered(
            lambda x: x.product_id.life_time
        ):
            lots = []
            for move_line in move.mapped('move_line_ids').filtered(
                lambda x: x.lot_id.life_date and datetime.today() + timedelta(
                    days=x.product_id.life_time
                ) > fields.Datetime.from_string(x.lot_id.life_date)
            ):
                if move_line.lot_id.name not in lots:
                    lots.append(move_line.lot_id.name)
            if move.name not in exceed:
                exceed[move.name] = lots
            else:
                exceed[move.name] += lots
        if exceed:
            exceed_error = ''
            for key in exceed:
                exceed_error += str(key) + ' - ' + str(exceed[key]).replace(
                    "'", '').replace('[', '').replace(']', '') + '\n'
            raise UserError(
                _(
                    'The next lots exceed the product life time:\n' +
                    exceed_error
                )
            )
