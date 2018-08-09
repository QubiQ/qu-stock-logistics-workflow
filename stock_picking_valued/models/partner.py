# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# Copyright (c) 2018 QubiQ (http://www.qubiq.es)

from odoo import models, fields


class resPartner(models.Model):
    _inherit = 'res.partner'

    valued_picking = fields.Boolean(string="Print valued picking",
                                    help="If checked It will print valued "
                                    "picks for this customer")
