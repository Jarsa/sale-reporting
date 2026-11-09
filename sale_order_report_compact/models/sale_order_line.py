# Copyright 2026 Jarsa
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)
from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _get_compact_report_description(self):
        """First line of the line description, without the internal reference.

        The description is the one edited by the salesperson; the internal
        reference is dropped because the report prints it in its own column.
        """
        self.ensure_one()
        name = (self.name or "").strip().split("\n")[0].strip()
        code = self.product_id.default_code
        if code and name.startswith(f"[{code}]"):
            name = name[len(code) + 2 :].strip()
        if not name and self.product_id:
            product = self.product_id.with_context(display_default_code=False)
            name = product.display_name
        return name
