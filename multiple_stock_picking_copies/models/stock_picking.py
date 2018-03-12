# -*- coding: utf-8 -*-
# Copyright (c) 2017 QubiQ (http://www.qubiq.es)
#                    Xavier Jiménez <xavier.jimenez@qubiq.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class StockPicking(models.Model):
    _inherit = "stock.picking"

    num_copies = fields.Integer(string="Number of copies", default=1)

    @api.multi
    def print_multiple_copies_picking(self):
        self.ensure_one()
        stock_picking_copies_ids = []
        num_copies = self.num_copies

        while(num_copies > 0):
            stock_picking_copies_ids.append(self.id)
            num_copies -= 1

        stock_picking_obj = self.env['stock.picking'].browse(
            stock_picking_copies_ids)

        return self.env['report'].get_action(
            stock_picking_obj, 'stock.report_picking')
