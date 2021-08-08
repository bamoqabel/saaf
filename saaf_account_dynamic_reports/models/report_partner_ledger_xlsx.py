# _*_ coding: utf-8
from odoo import models, fields, api, _


class InsPartnerLedgerXlsx(models.AbstractModel):
    _inherit = 'report.dynamic_xlsx.ins_partner_ledger_xlsx'

    def prepare_report_contents(self, data, acc_lines, filter):
        data = data[0]
        self.row_pos += 3

        if filter.get('include_details', False):
            self.sheet.write_string(self.row_pos, 0, _('Date'),
                                    self.format_header)
            self.sheet.write_string(self.row_pos, 1, _('JRNL'),
                                    self.format_header)
            self.sheet.write_string(self.row_pos, 2, _('Partner'),
                                    self.format_header)
            # self.sheet.write_string(self.row_pos, 3, _('Ref'),
            #                         self.format_header)
            self.sheet.write_string(self.row_pos, 3, _('Move'),
                                    self.format_header)
            self.sheet.write_string(self.row_pos, 4, _('Delivery Address'),
                                    self.format_header)
            self.sheet.write_string(self.row_pos, 5, _('Reference'),
                                    self.format_header)
            self.sheet.write_string(self.row_pos, 6, _('Debit'),
                                    self.format_header)
            self.sheet.write_string(self.row_pos, 7, _('Credit'),
                                    self.format_header)
            self.sheet.write_string(self.row_pos, 8, _('Balance'),
                                    self.format_header)
        else:
            self.sheet.merge_range(self.row_pos, 0, self.row_pos, 4, _('Partner'), self.format_header)
            self.sheet.write_string(self.row_pos, 5, _('Debit'),
                                    self.format_header)
            self.sheet.write_string(self.row_pos, 6, _('Credit'),
                                    self.format_header)
            self.sheet.write_string(self.row_pos, 7, _('Balance'),
                                    self.format_header)

        if acc_lines:
            for line in acc_lines:
                self.row_pos += 1
                self.sheet.merge_range(self.row_pos, 0, self.row_pos, 4, acc_lines[line].get('name') +'   ' + (acc_lines[line].get('mobile') if acc_lines[line].get('mobile',False) else '/'), self.line_header)
                self.sheet.write_number(self.row_pos, 5, float(acc_lines[line].get('debit')), self.line_header)
                self.sheet.write_number(self.row_pos, 6, float(acc_lines[line].get('credit')), self.line_header)
                self.sheet.write_number(self.row_pos, 7, float(acc_lines[line].get('balance')), self.line_header)

                if filter.get('include_details', False):

                    count, offset, sub_lines = self.record.build_detailed_move_lines(offset=0, partner=line,
                                                                                     fetch_range=1000000)

                    for sub_line in sub_lines:
                        if sub_line.get('move_name') == 'Initial Balance':
                            self.row_pos += 1
                            self.sheet.write_string(self.row_pos, 4, sub_line.get('move_name'),
                                                    self.line_header_light_initial)
                            self.sheet.write_number(self.row_pos, 5, float(sub_line.get('debit')),
                                                    self.line_header_light_initial)
                            self.sheet.write_number(self.row_pos, 6, float(sub_line.get('credit')),
                                                    self.line_header_light_initial)
                            self.sheet.write_number(self.row_pos, 7, float(sub_line.get('balance')),
                                                    self.line_header_light_initial)
                        elif sub_line.get('move_name') not in ['Initial Balance','Ending Balance']:
                            self.row_pos += 1
                            self.sheet.write_datetime(self.row_pos, 0, self.convert_to_date(sub_line.get('ldate')),
                                                    self.line_header_light_date)
                            self.sheet.write_string(self.row_pos, 1, sub_line.get('lcode'),
                                                    self.line_header_light)
                            self.sheet.write_string(self.row_pos, 2, sub_line.get('account_name') or '',
                                                    self.line_header_light)
                            # self.sheet.write_string(self.row_pos, 3, sub_line.get('lref') or '',
                            #                         self.line_header_light)
                            self.sheet.write_string(self.row_pos, 3, sub_line.get('move_name'),
                                                    self.line_header_light)
                            self.sheet.write_string(self.row_pos, 4, sub_line.get('delivery_address') if sub_line.get('delivery_address') else '/',
                                                    self.format_header)
                            self.sheet.write_string(self.row_pos, 5, sub_line.get('ref') if sub_line.get('ref') else '/',
                                                    self.format_header)
                            self.sheet.write_number(self.row_pos, 6,
                                                    float(sub_line.get('debit')),self.line_header_light)
                            self.sheet.write_number(self.row_pos, 7,
                                                    float(sub_line.get('credit')),self.line_header_light)
                            self.sheet.write_number(self.row_pos, 8,
                                                    float(sub_line.get('balance')),self.line_header_light)
                        else: # Ending Balance
                            self.row_pos += 1
                            self.sheet.write_string(self.row_pos, 4, sub_line.get('move_name'),
                                                    self.line_header_light_ending)
                            self.sheet.write_number(self.row_pos, 5, float(acc_lines[line].get('debit')),
                                                    self.line_header_light_ending)
                            self.sheet.write_number(self.row_pos, 6, float(acc_lines[line].get('credit')),
                                                    self.line_header_light_ending)
                            self.sheet.write_number(self.row_pos, 7, float(acc_lines[line].get('balance')),
                                                    self.line_header_light_ending)