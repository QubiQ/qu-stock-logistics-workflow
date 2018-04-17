# -*- coding: utf-8 -*-
# Copyright 2018 valentin vinagre <valentin.vinagre@qubiq.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import models, api


class StockInventory(models.Model):
    _inherit = "stock.inventory"

    @api.multi
    def action_done(self):
        res = super(StockInventory, self).action_done()
        for sel in self:
            sel.line_ids._quant_cost()
        return res
