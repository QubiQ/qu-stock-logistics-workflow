# -*- coding: utf-8 -*-
# Copyright 2018 valentin vinagre <valentin.vinagre@qubiq.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import fields, models, api, SUPERUSER_ID, _
import odoo.addons.decimal_precision as dp


class InventoryLine(models.Model):
    _inherit = "stock.inventory.line"

    cost = fields.Float(
        string=_('Unit Cost'),
        default=0.0,
        digits_compute=dp.get_precision('Product Price')
    )

    def _get_move_values(self, qty, location_id, location_dest_id):
        res = super(InventoryLine, self)._get_move_values(
            qty=qty,
            location_id=location_id,
            location_dest_id=location_dest_id)
        res['inventory_line'] = self.id
        return res

    @api.multi
    def _quant_cost(self):
        for sel in self.filtered(
           lambda r: r.product_qty - r.theoretical_qty > 0):
            self.env(user=SUPERUSER_ID)['stock.move'].\
                search([('inventory_line', '=', sel.id)]).\
                quant_ids.write({'cost': sel.cost})
