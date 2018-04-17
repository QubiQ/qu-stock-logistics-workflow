# -*- coding: utf-8 -*-
# Copyright 2018 valentin vinagre <valentin.vinagre@qubiq.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import models, fields, _


class StockMove(models.Model):
    _inherit = "stock.move"

    inventory_line = fields.Many2one(
        'stock.inventory.line',
        string=_('inventory line')
        )
