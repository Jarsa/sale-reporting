This module adds a second printout to quotations and sale orders,
*Quotation / Order (Internal)*, meant to be printed by the internal team.

It is a minimalist and compact document:

- Internal layout (no company logo, no address blocks, no decorative
  elements) and a paper format with reduced margins.
- Small font size and one row per product line.
- No product images, even when another module (for example
  `sale_order_report_product_image`) adds them to the customer printout.

Columns: line number, internal reference, short description (product name
without the internal reference), quantity, unit of measure, unit price,
discount (only when at least one line has a discount) and subtotal.
Sections and notes are printed as single rows. Untaxed amount, taxes and
total are shown at the end.

The customer printout (*Quotation / Order*) is not modified.
