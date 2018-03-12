# -*- coding: utf-8 -*-
# Copyright (c) 2017 QubiQ (http://www.qubiq.es)
#                    Xavier Jiménez <xavier.jimenez@qubiq.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api
from openerp.exceptions import ValidationError


class MassCancelProcurementOrder(models.TransientModel):
    _name = 'mass.cancel.procurement.order'

    @api.multi
    def cancel(self):
        active_ids = self.env.context.get('active_ids', [])
        proc_obj = self.env['procurement.order'].search([(
            'id', 'in', active_ids)])

        for po in proc_obj:
            if po.state == 'exception':
                po.state = 'cancel'
            else:
                raise ValidationError('A procurement order selected is not \
                    on exception state !')
