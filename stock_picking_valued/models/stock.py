# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# Copyright (c) 2018 QubiQ (http://www.qubiq.es)

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class stock_picking(models.Model):

    _inherit = "stock.picking"

    amount_untaxed = fields.Float(
        compute='_amount_all',
        digits=dp.get_precision('Account'),
        string='Untaxed Amount',
        readonly=True,
        store=True,
    )
    amount_tax = fields.Float(
        compute='_amount_all',
        digits=dp.get_precision('Account'),
        string='Taxes',
        readonly=True,
        store=True,
    )
    amount_total = fields.Float(
        compute='_amount_all',
        digits=dp.get_precision('Account'),
        string='Total',
        readonly=True,
        store=True,
    )
    amount_gross = fields.Float(
        compute='_amount_all',
        digits=dp.get_precision('Account'),
        string='amount gross',
        readonly=True,
        store=True,
    )
    amount_discounted = fields.Float(
        compute='_amount_all',
        digits=dp.get_precision('Account'),
        string='amount discounted',
        readonly=True,
        store=True,
    )
    external_note = fields.Text('External Notes')
    valued_picking = fields.Boolean(
        string="Print valued picking",
        help="If checked It will print valued "
        "picks for this customer",
    )
    currency_id = fields.Many2one(
        'res.currency',
        compute='_amount_all',
        string="Currency",
        readonly=True,
        store=True,
    )

    @api.multi
    @api.depends('move_lines', 'partner_id')
    def _amount_all(self):
        for picking in self:
            sale_id = picking.sale_id
            purchase_id = picking.purchase_id
            taxes = amount_gross = amount_untaxed = 0.0
            cur = picking.partner_id.property_product_pricelist \
                and picking.partner_id.property_product_pricelist.currency_id \
                or False
            if sale_id:
                picking.currency_id = sale_id.pricelist_id.currency_id
            elif purchase_id:
                picking.currency_id = purchase_id.currency_id

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

    @api.multi
    def _get_tax_amount_by_group(self):
        self.ensure_one()
        res = {}
        for line in self.move_lines:
            base_tax = 0
            for tax in line.tax_id:
                group = tax.tax_group_id
                res.setdefault(group, {'amount': 0.0, 'base': 0.0})
                # FORWARD-PORT UP TO SAAS-17
                price_reduce = line.order_price_unit
                taxes = tax.compute_all(
                    price_reduce + base_tax,
                    quantity=line.product_uom_qty,
                    product=line.product_id,
                    partner=self.partner_id)['taxes']
                for t in taxes:
                    res[group]['amount'] += t['amount']
                    res[group]['base'] += t['base']
                if tax.include_base_amount:
                    base_tax += tax.compute_all(
                        price_reduce + base_tax, quantity=1,
                        product=line.product_id,
                        partner=self.partner_id)['taxes'][0]['amount']
        res = sorted(res.items(), key=lambda l: l[0].sequence)
        res = [(
            l[0].name, l[1]['amount'], l[1]['base'], len(res)) for l in res]
        return res


class stock_move(models.Model):

    _inherit = "stock.move"

    price_subtotal = fields.Float(
        compute='_get_subtotal',
        string="Subtotal",
        digits=dp.get_precision('Account'),
        readonly=True,
        store=True,
        multi=True,
    )
    order_price_unit = fields.Float(
        compute='_get_subtotal',
        string="Price unit",
        digits=dp.get_precision('Product Price'),
        readonly=True,
        store=True,
        multi=True,
    )
    cost_subtotal = fields.Float(
        compute='_get_subtotal',
        string="Cost subtotal",
        digits=dp.get_precision('Account'),
        readonly=True,
        store=True,
        multi=True,
    )
    margin = fields.Float(
        compute='_get_subtotal',
        string="Margin",
        digits=dp.get_precision('Account'),
        readonly=True,
        store=True,
        multi=True,
    )
    percent_margin = fields.Float(
        compute='_get_subtotal',
        string="% margin",
        digits=dp.get_precision('Account'),
        readonly=True,
        store=True,
        multi=True,
    )
    tax_id = fields.Many2many(
        'account.tax',
        string='Taxes',
        compute='_get_subtotal',
        readonly=True,
        store=True,
        multi=True,
    )

    @api.multi
    @api.depends('product_id', 'product_uom_qty')
    def _get_subtotal(self):

        for move in self:
            price_unit = 0.0

            p_line_id = move.purchase_line_id
            s_line_id = move.sale_line_id
            if s_line_id:
                price_unit = (s_line_id.price_unit *
                              (1-(s_line_id.discount or 0.0)/100.0))
                move.tax_id = s_line_id.tax_id
            elif p_line_id:
                price_unit = (p_line_id.price_unit *
                              (1-(p_line_id.discount or 0.0)/100.0))
                move.tax_id = p_line_id.taxes_id
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
        compute='_get_subtotal',
        string="Subtotal",
        digits=dp.get_precision('Account'),
        readonly=True,
        store=False,
    )

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
