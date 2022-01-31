import xlsxwriter
from datetime import datetime
import datetime
from reports.report_utils import ReportUtility

utils = ReportUtility()


class SeparateReportXLs:

    def write_data_xls(self, data_dict,from_date,to_date):
        x = datetime.datetime.now()
        date_time_str = x.strftime("%d_%m_%YT%H_%M_%S")
        file_name = "xls_data_" + utils.gen_random() + str(date_time_str + ".xlsx")
        workbook = xlsxwriter.Workbook(str(utils.get_report_path()) + file_name)
        for sheet_name, values_dict in data_dict.items():
            self.write_query_records(workbook, values_dict, sheet_name, from_date,to_date)
        workbook.close()
        return file_name

    def write_query_records(self, workbook, data_dict, sheetName, from_date,to_date):
        try:
            header_list = data_dict.get("report_headers")
            del data_dict["report_headers"]
            worksheet = workbook.add_worksheet(sheetName)
            worksheet.merge_range('A1:D3', "")
            worksheet.write('H1', "Generated on: "+str(utils.getDateTime()))
            worksheet.write('H2', "Begin: " + str(from_date))
            worksheet.write('H3', "End: " + str(to_date))
            header_format = workbook.add_format({'bold': True, 'bg_color': '#e6e6e6', "align": "center"})
            event_format = workbook.add_format({'bold': True, 'bg_color': '#999999'})
            # worksheet.insert_image('A1', utils.get_poly_logo() + 'poly_report_logo.JPG', {'x_scale': 0.3, 'y_scale': 0.2})
            worksheet.insert_image('A1', utils.get_poly_logo() + 'poly_report_logo.jpg', {'x_scale': 1, 'y_scale': 0.8})
            row = 5
            if len(data_dict) > 0:
                for key, value in data_dict.items():
                    column = 0
                    # worksheet.write(row, column, str(key), event_format)
                    worksheet.merge_range("A"+str(row+1)+":F"+str(row+1)+"",str(key), event_format)
                    row += 1
                    for header in header_list:
                        width = len(str(header)) + 2
                        worksheet.set_column(row, column, width)
                        worksheet.write(row, column, header, header_format)
                        column += 1
                    row += 1
                    for rows in value:
                        d_column = 0
                        for dt in rows:
                            worksheet.write(row, d_column, dt)
                            d_column += 1
                        row += 1
                    row += 1
            else:
                worksheet.merge_range("A" + str(row + 1) + ":F" + str(row + 1) + "", str("No Data Found"), event_format)
            return "success", "success"
        except Exception as ex:
            print("Exception while writing xls file:  " + str(ex))
            return "Exception while writing xls file:  " + str(ex), "error"
