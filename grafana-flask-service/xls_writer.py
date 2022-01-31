import xlsxwriter
import os
import random
import string
from datetime import datetime
import datetime

script_path = os.path.abspath(__file__)
folder_path = os.path.split(script_path)
file_path = str(os.path.join(folder_path[0], 'saved_xls/'))


class XlsWriter:
    def write_data_xls(self, data_dict):
        x = datetime.datetime.now()
        date_time_str = x.strftime("%d_%m_%YT%H_%M_%S")
        file_name = "xls_data_" + self.gen_random() + str(date_time_str + ".xlsx")
        workbook = xlsxwriter.Workbook(str(file_path) + file_name)
        for sheet_name, values_list in data_dict.items():
            self.write_query_records(workbook, values_list, sheet_name)
        workbook.close()
        return file_name

    def write_query_records(self, workbook, data_list, sheetName):
        try:
            header_list = data_list[0]
            worksheet = workbook.add_worksheet(sheetName)
            header_format = workbook.add_format(
                {'bold': True, 'bg_color': '#9fbfdf', "align": "center"})
            row = 0
            column = 0
            for header in header_list:
                width = len(str(header))
                worksheet.set_column(row, column, 35)
                worksheet.write(row, column, header, header_format)
                column += 1
            row += 1
            flag = True
            for data in data_list:
                if flag:
                    flag = False
                    continue
                d_column = 0
                for rows in data:
                    # width = len(str(rows))
                    # worksheet.set_column(row, d_column, width)
                    worksheet.write(row, d_column, rows)
                    d_column += 1
                row += 1
            return "success", "success"
        except Exception as ex:
            print("Exception while writing xls file:  " + str(ex))
            return "Exception while writing xls file:  " + str(ex), "error"

    def gen_random(self):
        keylist = [random.choice(
            (string.ascii_letters + string.digits)) for i in range(20)]
        return str(("".join(keylist)))

# xls = XlsWriter()
# xls.write_data_xls([[1,2],[2,3]])
