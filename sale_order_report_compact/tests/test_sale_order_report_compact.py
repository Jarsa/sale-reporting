# Copyright 2026 Jarsa
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)
import base64

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

PIXEL = base64.b64encode(
    base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    )
)
REPORT = "sale_order_report_compact.report_saleorder_compact"
ACTION = "sale_order_report_compact.action_report_saleorder_compact"


@tagged("post_install", "-at_install")
class TestSaleOrderReportCompact(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "Compact Customer"})
        cls.product = cls.env["product.product"].create(
            {
                "name": "Compact Widget",
                "default_code": "CMP-001",
                "list_price": 100.0,
                "image_1920": PIXEL,
            }
        )
        cls.order = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner.id,
                "client_order_ref": "PO-REF-42",
                "order_line": [
                    (0, 0, {"display_type": "line_section", "name": "Main Section"}),
                    (
                        0,
                        0,
                        {
                            "product_id": cls.product.id,
                            "name": "[CMP-001] Compact Widget\nLong sales description",
                            "product_uom_qty": 3.0,
                            "price_unit": 100.0,
                        },
                    ),
                    (0, 0, {"display_type": "line_note", "name": "Internal note"}),
                ],
            }
        )

    def _render(self, order):
        html, _ = self.env["ir.actions.report"]._render_qweb_html(REPORT, order.ids)
        return html.decode()

    def test_report_action_bound_to_sale_order(self):
        action = self.env.ref(
            "sale_order_report_compact.action_report_saleorder_compact"
        )
        self.assertEqual(action.binding_model_id.model, "sale.order")
        self.assertEqual(action.binding_type, "report")
        self.assertEqual(action.paperformat_id.margin_left, 7)

    def test_report_content_without_images(self):
        html = self._render(self.order)
        self.assertIn("CMP-001", html)
        self.assertIn("Compact Widget", html)
        self.assertNotIn("Long sales description", html)
        self.assertIn("PO-REF-42", html)
        self.assertIn("Main Section", html)
        self.assertIn("Internal note", html)
        self.assertNotIn("<img", html)
        self.assertNotIn("/web/image", html)
        self.assertNotIn("image_128", html)
        self.assertNotIn('name="th_discount"', html)

    def test_report_discount_column(self):
        self.order.order_line.filtered("product_id").discount = 10.0
        html = self._render(self.order)
        self.assertIn('name="th_discount"', html)

    def test_customer_report_unchanged(self):
        html, _ = self.env["ir.actions.report"]._render_qweb_html(
            "sale.report_saleorder", self.order.ids
        )
        self.assertIn("Long sales description", html.decode())
