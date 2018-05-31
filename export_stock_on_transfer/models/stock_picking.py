# -*- coding: utf-8 -*-
# Copyright 2018 Xavier Jiménez <xavier.jimenez@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import models, api
import logging

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = "stock.picking"

    # Function to get a list with the product templates within a picking
    # and update the stock to PrestaShop after the transfer
    @api.multi
    def do_transfer(self):
        res = super(StockPicking, self).do_transfer()
        ps_product_obj = self.env['prestashop.product.combination']

        for picking in self:
            for move in picking.move_lines:
                # Only update if the transfer is on the main WH
                update_ps_stock = False

                # Incoming
                if picking.picking_type_id.code == 'incoming':
                    # WH/Stock
                    if picking.location_dest_id.id == 12:
                        update_ps_stock = True
                # Outgoing
                if picking.picking_type_id.code == 'outgoing':
                    # WH/Stock
                    if picking.location_id.id == 12:
                        update_ps_stock = True

                if update_ps_stock:
                    if move.product_id.type == 'product':
                        ps_product_obj = ps_product_obj.search([(
                            'odoo_id', '=', move.product_id.id)])
                        ps_product_obj.recompute_prestashop_qty()

        return res
