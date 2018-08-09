# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# Copyright (c) 2018 QubiQ (http://www.qubiq.es)

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class stock_picking(models.Model):

    _inherit = "stock.picking"

    amount_untaxed = fields.Float(
        compute='_amount_all', digits=dp.get_precision('Account'),
        string='Untaxed Amount', readonly=True, store=True)
    amount_tax = fields.Float(
        compute='_amount_all', digits=dp.get_precision('Account'),
        string='Taxes', readonly=True, store=True)
    amount_total = fields.Float(
        compute='_amount_all', digits=dp.get_precision('Account'),
        string='Total', readonly=True, store=True)
    amount_gross = fields.Float(
        compute='_amount_all', digits=dp.get_precision('Account'),
        string='amount gross', readonly=True, store=True)
    amount_discounted = fields.Float(
        compute='_amount_all', digits=dp.get_precision('Account'),
        string='amount discounted', readonly=True, store=True)
    external_note = fields.Text(
        ' External Notes')
    valued_picking = fields.Boolean(string="Print valued picking",
                                    help="If checked It will print valued "
                                    "picks for this customer")

    @api.multi
    @api.depends('move_lines', 'partner_id')
    def _amount_all(self):
        for picking in self:
            taxes = amount_gross = amount_untaxed = 0.0
            cur = picking.partner_id.property_product_pricelist \
                and picking.partner_id.property_product_pricelist.currency_id \
                or False
            for line in picking.move_lines:
                price_unit = 0.0
                order_line = False
                if line.sale_line_id and line.state != 'cancel':
                    order_line = line.sale_line_id
                    taxes_obj = order_line.tax_id
                elif line.purchase_line_id and line.state != 'cancel':
                    order_line = line.purchase_line_id
                    taxes_obj = order_line.taxes_id
                else:
                    continue

                price_unit = order_line.price_unit * \
                    (1 - (order_line.discount or 0.0) / 100.0)
                for c in taxes_obj.compute_all(
                        price_unit=price_unit, quantity=line.product_uom_qty,
                        product=line.product_id,
                        partner=order_line.order_id.partner_id)['taxes']:
                    taxes += c.get('amount', 0.0)
                amount_gross += (order_line.price_unit *
                                 line.product_uom_qty)
                amount_untaxed += price_unit * line.product_uom_qty

            if cur:
                picking.amount_tax = cur.round(taxes)
                picking.amount_untaxed = cur.round(amount_untaxed)
                picking.amount_gross = cur.round(amount_gross)
            else:
                picking.amount_tax = round(taxes, 2)
                picking.amount_untaxed = round(amount_untaxed, 2)
                picking.amount_gross = round(amount_gross, 2)

            picking.amount_total = picking.amount_untaxed + picking.amount_tax
            picking.amount_discounted = picking.amount_gross - \
                picking.amount_untaxed


class stock_move(models.Model):

    _inherit = "stock.move"

    price_subtotal = fields.Float(
        compute='_get_subtotal', string="Subtotal",
        digits=dp.get_precision('Account'), readonly=True,
        store=True, multi=True)
    order_price_unit = fields.Float(
        compute='_get_subtotal', string="Price unit",
        digits=dp.get_precision('Product Price'), readonly=True,
        store=True, multi=True)
    cost_subtotal = fields.Float(
        compute='_get_subtotal', string="Cost subtotal",
        digits=dp.get_precision('Account'), readonly=True,
        store=True, multi=True)
    margin = fields.Float(
        compute='_get_subtotal', string="Margin",
        digits=dp.get_precision('Account'), readonly=True,
        store=True, multi=True)
    percent_margin = fields.Float(
        compute='_get_subtotal', string="% margin",
        digits=dp.get_precision('Account'), readonly=True,
        store=True, multi=True)

    @api.multi
    @api.depends('product_id', 'product_uom_qty')
    def _get_subtotal(self):

        for move in self:
            purchase_id = move.purchase_line_id
            price_unit = 0.0
            if move.sale_line_id:
                price_unit = (move.sale_line_id.price_unit *
                              (1-(move.sale_line_id.discount or 0.0)/100.0))
            elif purchase_id:
                price_unit = (purchase_id.price_unit *
                              (1-(purchase_id.discount or 0.0)/100.0))
            else:
                continue

            cost_price = move.product_id.lst_price or 0.0
            move.price_subtotal = price_unit * move.product_uom_qty
            move.order_price_unit = price_unit
            move.cost_subtotal = cost_price * move.product_uom_qty
            move.margin = move.price_subtotal - move.cost_subtotal
            if move.price_subtotal > 0:
                move.percent_margin = (move.margin/move.price_subtotal)*100
            else:
                move.percent_margin = 0


class StockMoveLine(models.Model):

    _inherit = 'stock.move.line'

    price_subtotal = fields.Float(
        compute='_get_subtotal', string="Subtotal",
        digits=dp.get_precision('Account'), readonly=True, store=False)

    @api.multi
    @api.depends('product_qty')
    def _get_subtotal(self):
        for line in self:
            move_ant_id = []
            subtotal = 0.0
            for move in line.move_id:
                if move.id not in move_ant_id:
                    move_ant_id.append(move.id)
                    price_unit = move.order_price_unit
                    subtotal += price_unit * move.product_uom_qty
            line.price_subtotal = subtotal
