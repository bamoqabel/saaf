# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.
import xlsxwriter
import base64
import tempfile
from datetime import datetime,date
from dateutil.relativedelta import relativedelta
from odoo import api, models, fields, _
from odoo.exceptions import ValidationError,Warning
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
import io


class CustomerSalesperonsReport(models.TransientModel):
    _name = "customers.salespersons.moves.report"

    name = fields.Char(string="Report Name", required=True, default="حركات عملاء بالمناديب")
    date_from = fields.Date(string='من', default=lambda *a: fields.Date.today() + relativedelta(day=1), required=False)
    date_to = fields.Date(string='إلى', default=lambda *a: fields.Date.today() + relativedelta(day=1, months=+1, days=-1), required=False)
    company_id = fields.Many2one('res.company', 'شركة', required=True, default=lambda self: self.env.company)
    user_ids = fields.Many2many('res.users', string='مندوب',relation="user_ids_rel", column1="user_ids_col1",column2="user_ids_col2")
    customer_ids = fields.Many2many('res.partner', string='عميل',relation="customer_id_rel", column1="customer_id_col1",column2="customer_id_col2")

    @api.constrains("date_from", "date_to")
    def _check_dates(self):
        if self.date_from and self.date_to:
            if self.date_from > self.date_to:
                raise Warning(_('Date From Cannot Be Greater Than Date TO!'))

    def print_customers_salespersons_moves_report_pdf_report(self):
        self.ensure_one()
        data={}
        data_list_company = []
        data_list_person = []
        so_domain = [('state', 'in', ('sale', 'done')),('company_id','=',self.company_id.id),]

        if self.customer_ids:
            customers = self.customer_ids
        else:
            customers = self.env['res.partner'].sudo().search([],order='is_company')
        if self.user_ids:
            so_domain.append(('user_id', 'in', self.user_ids.ids),)
        for customer in customers :
            print("customer",customer.name)
            so_domain.append(('partner_id', '=', customer.id),)
            print("so_domain",so_domain)
            so_records = self.env['sale.order'].sudo().search(so_domain)
            for so in so_records:
                print("so", so.name)
                container_counter = 0.0
                containers ,service_numbers,delivery_addresses = '','',''
                invoice_ids = self.env['account.move'].sudo().search([('id','in',so.invoice_ids.ids)],limit=1)
                picking_ids = self.env['stock.picking'].sudo().search([('id','in',so.picking_ids.ids),])
                for picking in picking_ids:
                    for container in picking.container_id:
                        container_counter += 1
                    for container in picking.container_id:
                        containers += container.number + '/' +  container.name + ' , '
                    if picking.service_number:
                        service_numbers += picking.service_number + ' , '
                    if picking.partner_id:
                        delivery_addresses += picking.partner_id.display_name + ' , '
                if customer.is_company == True:
                    data_list_company.append({
                        'customer': so.partner_id.display_name,
                        'container_counter': container_counter,
                        'containers': containers,
                        'service_numbers': service_numbers,
                        'delivery_addresses': delivery_addresses,
                        'so_total': so.amount_total,
                        'inv_total': invoice_ids.amount_total if invoice_ids else 0,
                        'amount_residual': invoice_ids.amount_residual if invoice_ids else 0,
                    })
                else:
                    data_list_person.append({
                        'customer': so.partner_id.display_name,
                        'container_counter': container_counter,
                        'containers': containers,
                        'service_numbers': service_numbers,
                        'delivery_addresses': delivery_addresses,
                        'so_total': so.amount_total,
                        'inv_total': invoice_ids.amount_total if invoice_ids else 0,
                        'amount_residual': invoice_ids.amount_residual if invoice_ids else 0,
                    })
            so_domain.remove(('partner_id', '=', customer.id))


        filters = []
        filters.append({
            'customer_ids': ', '.join(self.customer_ids.mapped('name')) if self.customer_ids else 'الكل',
            'user_ids': ', '.join(self.user_ids.mapped('name')) if self.user_ids else 'الكل',
            'date_from': self.date_from if self.date_from else '',
            'date_to': self.date_to if self.date_to else '',
            'company_id': self.company_id.name,
            'name': self.name,
        })

        data['data_list_person'] = data_list_person
        data['data_list_company'] = data_list_company
        data['filters'] = filters
        return self.env.ref('inventory_containers.customers_salespersons_moves_report_template_id').report_action(self, data=data)

