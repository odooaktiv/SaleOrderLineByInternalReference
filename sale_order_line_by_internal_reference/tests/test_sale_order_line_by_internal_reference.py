# -*- coding: utf-8 -*-

from odoo.tests import common


class TestSaleOrderLine(common.TransactionCase):
    """Test onchange for product code in sale order."""

    def test_sale_order_line_by_internal_reference(self):
        """Create Sale Order and call onchange of default code."""
        sale_order = self.env.ref('sale.sale_order_1')
        product = self.env.ref('product.product_product_7')

        sale_order.write({'default_code': product.default_code})

        sale_order.onchange_default_code()
        new_order_line = sale_order.order_line.search([
            ('order_id', '=', sale_order.id),
            ('product_id.default_code', '=', product.default_code)], limit=1)
        self.assertEquals(
            product.default_code, new_order_line.product_id.default_code,
            "Product and Order Line's Reference should be same")
