# Copyright 2018 Xavier Piernas <xavier.piernas@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _


class ProductPackaging(models.Model):
    _inherit = 'product.packaging'

    package_length = fields.Float(
        string=_('Length')
    )
    package_height = fields.Float(
        string=_('Height')
    )
    package_width = fields.Float(
        string=_('Width')
    )
    package_volume = fields.Float(
        compute='_compute_volume',
        store=True,
        string=_('Volume'),
        readonly=True
    )

    @api.depends(
        'package_length', 'package_height', 'package_width'
    )
    @api.multi
    def _compute_volume(self):
        for sel in self:
            sel.package_volume =\
                sel.package_length * sel.package_height * sel.package_width
