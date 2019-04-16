# Copyright 2019 Xavier Piernas <xavier.piernas@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, api, _
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def split(self):
        for sel in self:
            if sel.state in ['done', 'cancel']:
                raise UserError(_(
                    'The picking cannot be in done or cancel state'
                ))
            pickings = self.env['stock.picking']
            for line in sel.move_lines:
                if line.location_dest_id != sel.location_dest_id:
                    target_picking = pickings.filtered(
                        lambda x: x.location_dest_id == line.location_dest_id
                    )
                    if not target_picking:
                        target_picking = sel.copy({
                            'move_lines': False,
                            'location_dest_id': line.location_dest_id.id,
                            'origin': sel.name
                        })
                        pickings += target_picking
                    line.picking_id = target_picking
            pickings += sel
        form_view = self.env.ref('stock.view_picking_form')
        tree_view = self.env.ref('stock.vpicktree')
        return {
            'name': _('Picking Lists'),
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking',
            'view_id': tree_view.id,
            'views': [(tree_view.id, 'tree'), (form_view.id, 'form')],
            'view_type': 'form',
            'view_mode': 'tree, form',
            'target': 'current',
            'domain': "[('id', 'in', %s)]" % (pickings.ids),
        }
