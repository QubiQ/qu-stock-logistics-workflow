# -*- coding: utf-8 -*-
# Copyright (c) 2017 QubiQ (http://www.qubiq.es)
#                    Xavier Jiménez <xavier.jimenez@qubiq.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.osv import fields, osv


class stock_inventory(osv.osv):
    _inherit = "stock.inventory"
    _description = "Inventory"

    _columns = {
        'exhausted': fields.boolean(
            'Incluir productos agotados',
            readonly=True,
            states={'draft': [('readonly', False)]})
    }
    _defaults = {
        'exhausted': False,
    }

    def _get_inventory_lines(self, cr, uid, inventory, context=None):
        location_obj = self.pool.get('stock.location')
        product_obj = self.pool.get('product.product')
        quant_products_list = []

        location_ids = location_obj.search(
            cr, uid, [(
                'id', 'child_of', [
                    inventory.location_id.id])], context=context)
        domain = ' location_id in %s'
        args = (tuple(location_ids),)
        if inventory.partner_id:
            domain += ' and owner_id = %s'
            args += (inventory.partner_id.id,)
        if inventory.lot_id:
            domain += ' and lot_id = %s'
            args += (inventory.lot_id.id,)
        if inventory.product_id:
            domain += ' and product_id = %s'
            args += (inventory.product_id.id,)
        if inventory.package_id:
            domain += ' and package_id = %s'
            args += (inventory.package_id.id,)

        cr.execute('''
           SELECT product_id, sum(qty) AS product_qty, location_id, lot_id
           AS prod_lot_id, package_id, owner_id AS partner_id
           FROM stock_quant WHERE''' + domain + '''
           GROUP BY product_id, location_id, lot_id, package_id, partner_id
        ''', args)
        vals = []
        for product_line in cr.dictfetchall():
            # replace the None the dictionary by False
            # because falsy values are tested later on
            for key, value in product_line.items():
                if not value:
                    product_line[key] = False
            product_line['inventory_id'] = inventory.id
            product_line['theoretical_qty'] = product_line['product_qty']
            if product_line['product_id']:
                product = product_obj.browse(
                    cr, uid, product_line['product_id'], context=context)
                product_line['product_uom_id'] = product.uom_id.id
                quant_products_list.append(product.id)
            vals.append(product_line)

        if inventory.exhausted:
            exhausted_vals = inventory._get_exhausted_inventory_line(
                inventory, quant_products_list)
            vals.extend(exhausted_vals)
        return vals

    def _get_exhausted_inventory_line(
            self, cr, uid, inventory, quant_products_list, context=None):
        product_obj = self.pool.get('product.product')
        vals = []
        exhausted_domain = [(
            'type', 'not in', ('service', 'consu', 'digital'))]
        if quant_products_list:
            exhausted_domain += [('id', 'not in', quant_products_list)]
        exhausted_products = product_obj.search(
            cr, uid, exhausted_domain, context=context)
        for product in exhausted_products:
            uom_id = product_obj.browse(cr, uid, product).uom_id.id
            vals.append({
                'inventory_id': inventory.id,
                'product_id': product,
                'location_id': inventory.location_id.id,
                'product_uom_id': uom_id,
            })
        return vals
