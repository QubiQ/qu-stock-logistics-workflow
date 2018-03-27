# -*- coding: utf-8 -*-

from odoo import models, api, _
from odoo.exceptions import UserError

import logging
logger = logging.getLogger(__name__)


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    @api.model
    def create(self, vals):
        lot_obj = self.search([('name', '=', vals['name'])])
        if lot_obj:
            raise UserError(_(
                'Some introduced lots are already defined for other products.'
                '\n\n Repeated lot: %s' % (lot_obj[0].name)))

        return super(StockProductionLot, self).create(vals)
