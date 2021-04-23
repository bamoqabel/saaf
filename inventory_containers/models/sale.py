from odoo import api, fields, models


class SaleAdvancePaymentInv(models.Model):
    _inherit= 'sale.order'
    service_number = fields.Char(string="رقم الخدمة", required=False, copy=False, readonly=True)


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def create_invoices(self):
        res = super(SaleAdvancePaymentInv, self).create_invoices()
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))

        for so in sale_orders:
            picking_ids = self.env['stock.picking'].sudo().search([('id', 'in', so.picking_ids.ids)])
            if picking_ids and any(picking_ids.mapped('service_number')):
                service_number = ', '.join(pick.service_number for pick in picking_ids if pick.service_number)
                so.service_number = service_number
                for inv in so.invoice_ids:
                    inv.ref = service_number
        return res
