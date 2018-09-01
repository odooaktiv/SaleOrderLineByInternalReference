# -*- coding: utf-8 -*-
# Part of AktivSoftware See LICENSE file for full copyright
# and licensing details.

from odoo import api, fields, models


class SaleOrder(models.Model):
    """Add default code field."""

    _inherit = "sale.order"

    default_code = fields.Char(
        "Product Internal Reference",
        help="Enter Internal Reference of product for fill Sale Order Line")

    @api.onchange('default_code')
    def onchange_default_code(self):
        """Fill Sale Order Line based on default code."""
        default_code_id = new_sale_order_line = False
        order_line_vals = {}
        if self.default_code:
            default_code_id = self.env['product.product'].search(
                [('default_code', '=', self.default_code)], limit=1)
            if default_code_id:
                order_line_vals.update({
                    'product_id': default_code_id.id,
                })
                flag = False
                if self.order_line:
                    for line in self.order_line:
                        if line.product_id.id == order_line_vals.get(
                                'product_id', False):
                            line.product_uom_qty += 1
                            flag = True
                            break
                if not flag:
                    new_sale_order_line = self.env[
                        'sale.order.line'].new(order_line_vals)
                    self.order_line += new_sale_order_line
                    new_sale_order_line.product_id_change()
        self.default_code = False
