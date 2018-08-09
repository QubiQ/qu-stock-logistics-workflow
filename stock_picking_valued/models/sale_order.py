# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# Copyright (c) 2018 QubiQ (http://www.qubiq.es)

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    valued_picking = fields.Boolean('Valued picking',
                                    help="If it sets to True, the picking will \
                                    be valued", readonly=True,
                                    states={'draft': [('readonly', False)]})

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            order.picking_ids.write({'valued_picking': order.valued_picking})
        return res

    @api.multi
    @api.onchange('partner_id')
    def valued_onchange_partner_id(self):
        values = {'valued_picking': False}
        if self.partner_id:
            values['valued_picking'] = self.partner_id.valued_picking or \
                self.partner_id.parent_id.valued_picking
        self.update(values)
