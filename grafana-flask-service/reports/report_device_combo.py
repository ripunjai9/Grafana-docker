import xlsxwriter
from datetime import datetime
import datetime
from reports.report_utils import ReportUtility

utils = ReportUtility()

class ReportXls:

    def list_to_string(self, s):
        # initialize an empty string
        str1 = ""
        # traverse in the string
        for ele in s:
            str1 += ele+ ', '

        return str1

    def format_bytes(self, size1):
        # 2**10 = 1024
        size = float(size1)
        power = 2 ** 10
        n = 0
        power_labels = {0: 'KB', 1: 'MB', 2: 'GB', 3: 'TB', 4: 'PB'}
        while size > power:
            if n == 4:
                break

            size /= power
            n += 1

        return str(round(size, 3))+' '+power_labels[n]

    def write_data_xls(self, data_dict,  header,  from_date, to_date):
        x = datetime.datetime.now()
        date_time_str = x.strftime("%d_%m_%YT%H_%M_%S")
        file_name = "xls_data_" + utils.gen_random() + str(date_time_str + ".xlsx")
        workbook = xlsxwriter.Workbook(str(utils.get_report_path()) + file_name)
        for sheet_name, values_list in header.items():
            self.write_query_records(workbook, data_dict, sheet_name, values_list, from_date, to_date)
        workbook.close()
        return file_name

    def write_query_records(self, workbook, data_dict, sheetName, header,  from_date, to_date):
        try:

            worksheet = workbook.add_worksheet(sheetName)
            worksheet.merge_range('A1:C3', "")
            worksheet.insert_image('A1', utils.get_poly_logo() + 'poly_report_logo.jpg', {'x_scale': 1, 'y_scale': 0.8})
            worksheet.write('H1', "Generated on: " + str(utils.getDateTime()))
            worksheet.write('H2', "Begin: " + str(from_date))
            worksheet.write('H3', "End: " + str(to_date))
            row = 5
            column = 0
            row += 1
            flag = True
            # print(data_dict)
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#808080',
                'align': 'center',
                'border_color': '#ffffff',
                'bold':True
            })
            header_format.set_border_color('#000000')
            merge_format = workbook.add_format({
                'bg_color': '#D3D3D3',
                'border_color': '#ffffff'
            })
            merge_format.set_border_color('#000000')
            data_format = workbook.add_format({

                'border_color': '#ffffff'
            })
            # print(header)
            worksheet.set_column('A:C', 25)
            worksheet.set_column('D:H', 15)

            ws2 = workbook.add_worksheet('Data')
            ws2_row = 0
            ws3 = workbook.add_worksheet('Data_available')
            ws3_row = 0
            ws4 = workbook.add_worksheet('mem_swap')
            ws4_row = 0
            format = workbook.add_format({'num_format': 'mmm yyyy'})
            for data in data_dict:
                tem_data = data_dict[data][0]
                if tem_data:
                    device = 'Device: '+str(tem_data[0])  # + ' ['+data+'] '
                    # device_information = header_list[1]
                    worksheet.merge_range('A'+str(row)+':H'+str(row), device, header_format)
                    row += 1
                    worksheet.merge_range('A'+str(row)+':H'+str(row), "Device Information", header_format)
                    # row += 1
                    worksheet.write(row, 0, "Device Class", merge_format)
                    worksheet.write(row, 1, tem_data[1])

                    worksheet.write(row, 2, "CUG", merge_format)
                    worksheet.write(row, 3, tem_data[4])

                    worksheet.write(row, 4, "Created Date", merge_format)
                    worksheet.write(row, 5, tem_data[7])

                    worksheet.write(row, 6, "Port Scan", merge_format)
                    worksheet.write(row, 7, tem_data[6])

                    row += 1
                    worksheet.write(row, 0, "Device Category", merge_format)
                    worksheet.write(row, 1, tem_data[2])

                    worksheet.write(row, 2, "Managed Type", merge_format)
                    worksheet.write(row, 3, tem_data[5])

                    worksheet.write(row, 4, "Active", merge_format)
                    worksheet.write(row, 5, tem_data[8])

                    worksheet.write(row, 6, "IP", merge_format)
                    worksheet.write(row, 7, tem_data[9])
                    row += 1

                    worksheet.write(row, 0, "Device Description", merge_format)
                    worksheet.write(row, 1, tem_data[3])
                    row += 1
                    # row += 1
                tem_ram_data = data_dict[data][1]
                tem_cpu_data = data_dict[data][2]
                tem_swap_data = data_dict[data][3]
                tem_avail_data = data_dict[data][4]
                if tem_ram_data or tem_cpu_data or tem_swap_data or tem_avail_data:
                    row += 1
                    # column = 1
                    worksheet.merge_range('A' + str(row) + ':H' + str(row), "Device Hardware", header_format)

                    worksheet.write(row, 0, "CPUs", merge_format)
                    worksheet.write(row, 1, "CPUs %used", merge_format)
                    worksheet.write(row, 2, "RAM size", merge_format)
                    worksheet.write(row, 3, "RAM used", merge_format)
                    worksheet.write(row, 4, "swap size", merge_format)
                    worksheet.write(row, 5, "swap%", merge_format)
                    worksheet.write(row, 6, "Availability", merge_format)
                    worksheet.write(row, 7, "Latency (ms)", merge_format)
                    row += 1
                    worksheet.write(row, 0, 0)
                    worksheet.write(row, 2, "MB")
                    worksheet.write(row, 4, "MB")

                    if tem_cpu_data :
                        worksheet.write(row, 1, str(round(float(tem_cpu_data[0]), 2))+'%')
                    if tem_ram_data:
                        worksheet.write(row, 3, str(round(float(tem_ram_data[0]), 2))+'%')
                    if tem_swap_data:
                        worksheet.write(row, 5, str(round(float(tem_swap_data[0]), 2))+'%')
                    if tem_avail_data:
                        worksheet.write(row, 6, str(round(float(tem_avail_data[0]), 2))+'%')
                        worksheet.write(row, 7, str(round(float(tem_avail_data[1]), 2)))
                    row += 1

                tem_port_data = self.list_to_string(data_dict[data][5])
                if tem_port_data:
                    row += 1

                    worksheet.merge_range('A' + str(row) + ':H' + str(row), "Ports", header_format)
                    device = header[0] + ': ' + str(tem_data[0])
                    # device_information = header_list[1]
                    worksheet.write(row, 0, "Open ports", merge_format)
                    row += 1
                    worksheet.merge_range('B' + str(row) + ':H' + str(row), str(tem_port_data), data_format)
                    row += 1

                tem_asset_data = data_dict[data][6]
                if tem_asset_data:
                    # row += 1
                    worksheet.merge_range('A' + str(row) + ':H' + str(row), "Asset Information", header_format)
                    worksheet.write(row, 0, "Make", merge_format)
                    worksheet.write(row, 1, tem_asset_data[0])
                    worksheet.write(row, 2, "Hostname", merge_format)
                    worksheet.write(row, 3, tem_asset_data[12])
                    worksheet.write(row, 4, "Function", merge_format)
                    worksheet.write(row, 5, tem_asset_data[14])
                    worksheet.write(row, 6, "Firmware Version", merge_format)
                    worksheet.write(row, 7, tem_asset_data[8])
                    row += 1

                    worksheet.write(row, 0, "Model", merge_format)
                    worksheet.write(row, 1, tem_asset_data[1])
                    worksheet.write(row, 2, "Serial Number", merge_format)
                    worksheet.write(row, 3, tem_asset_data[3])
                    worksheet.write(row, 4, "Host ID", merge_format)
                    worksheet.write(row, 5, tem_asset_data[5])
                    worksheet.write(row, 6, "Disk Array Size", merge_format)
                    worksheet.write(row, 7, tem_asset_data[11])
                    row += 1

                    worksheet.write(row, 0, "Operating System", merge_format)
                    worksheet.write(row, 1, tem_asset_data[13])
                    worksheet.write(row, 2, "Asset Tag", merge_format)
                    worksheet.write(row, 3, tem_asset_data[2])
                    worksheet.write(row, 4, "DNS Name", merge_format)
                    worksheet.write(row, 5, tem_asset_data[6])
                    worksheet.write(row, 6, "Disk count", merge_format)
                    worksheet.write(row, 7, tem_asset_data[9])
                    row += 1

                    worksheet.write(row, 2, "Asset type", merge_format)
                    worksheet.write(row, 3, tem_asset_data[4])
                    worksheet.write(row, 4, "DNS Domain", merge_format)
                    worksheet.write(row, 5, tem_asset_data[7])
                    worksheet.write(row, 6, "Disk Size", merge_format)
                    worksheet.write(row, 7, tem_asset_data[10])
                    row += 1

                temp_file_data = data_dict[data][7]

                if temp_file_data:
                    row += 1
                    worksheet.merge_range('A' + str(row) + ':H' + str(row), "File System Information", header_format)
                    row += 1
                    worksheet.merge_range('A' + str(row) + ':D' + str(row), "File System", merge_format)
                    row -= 1
                    worksheet.write(row, 4, "Size", merge_format)
                    worksheet.write(row, 5, "Space Used", merge_format)
                    worksheet.write(row, 6, "Space Available", merge_format)
                    worksheet.write(row, 7, "Used %", merge_format)

                    row += 1
                    for arr in temp_file_data:

                        if arr:
                            row += 1
                            worksheet.merge_range('A' + str(row) + ':D' + str(row), arr[0])
                            row -= 1
                            worksheet.write(row, 4, self.format_bytes(arr[1]))
                            worksheet.write(row, 5, self.format_bytes(arr[2]))
                            worksheet.write(row, 6, self.format_bytes(arr[3]))
                            worksheet.write(row, 7, str(arr[4]) + '%')
                        row += 1
                    row += 1

                temp_avg_ram_data = data_dict[data][8]
                if temp_avg_ram_data:
                    # print(data, temp_avg_ram_data)
                    ws2.write(ws2_row, 0, "month")
                    ws2.write(ws2_row, 1, "cpu avg")
                    row += 2
                    i = ws2_row

                    for val in temp_avg_ram_data:


                        date_month = datetime.datetime.strptime(val[0], "%Y-%m")
                        ws2_row += 1
                        # i+=1
                        ws2.write(ws2_row, 0, date_month, format)
                        ws2.write(ws2_row, 1, float(val[1]))

                    chart = workbook.add_chart({'type': 'line'})
                    chart.add_series({
                        'name': 'CPU Utilization % ',
                        'categories': ["Data", i+1, 0, ws2_row, 0],
                        'values': ["Data", i+1, 1, ws2_row, 1],
                        'marker': {'type': 'diamond'},
                    })
                    chart.set_x_axis({
                        'date_axis': True,
                        'name': 'Date'
                    })
                    chart.set_y_axis({
                        'name': 'Percentage',
                        'min': 0, 'max': 100
                    })
                    ws2_row += 2
                    worksheet.insert_chart('A'+str(row), chart)
                    row += 18
                # row += 2

                temp_avilab_data = data_dict[data][9]
                if temp_avilab_data:
                    ws2.write(ws3_row, 0, "month")
                    ws2.write(ws3_row, 1, "availability avg")
                    row += 2
                    i = ws3_row
                    for val in temp_avilab_data:
                        date_month = datetime.datetime.strptime((val[0]), "%Y-%m")
                        ws3_row += 1

                        # months = str(calendar.month_name[date_month.month])
                        ws3.write(ws3_row, 0, date_month, format)
                        ws3.write(ws3_row, 1, float(val[1]))

                    chart = workbook.add_chart({'type': 'line'})
                    chart.add_series({
                        'name': 'Availability',
                        'categories': ["Data_available", i+1, 0, ws3_row, 0],
                        'values': ["Data_available", i+1, 1, ws3_row, 1],
                        'marker': {'type': 'diamond'},
                    })
                    chart.set_x_axis({
                        'date_axis': True,
                        'name': 'Date'
                    })
                    chart.set_y_axis({
                        'name': 'Percentage',
                        'min': 0, 'max': 100
                    })

                    ws3_row += 2
                    worksheet.insert_chart('A'+str(row), chart)
                    row += 18

                mem_swap_dict = {}
                temp_mem_data = data_dict[data][11]
                temp_swap_data = data_dict[data][10]

                for value in temp_mem_data:
                    if mem_swap_dict.get(str(value[0])) is None:
                        mem_swap_dict[str(value[0])] = [value[1]]
                    else:
                        mem_swap_dict[str(value[0])].append(value[1])
                for val in temp_swap_data:
                    if mem_swap_dict.get(str(val[0])) is None:
                        # print(data)
                        mem_swap_dict[str(val[0])] = [0, val[1]]
                    else:
                        mem_swap_dict[str(val[0])].append(val[1])

                if temp_swap_data or temp_mem_data:
                    row += 2

                    ws4.write(ws4_row, 0, "month")
                    ws4.write(ws4_row, 1, "mem avg")
                    ws4.write(ws4_row, 2, "swap avg")
                    ws4_row += 1
                    i = ws4_row

                    for key in mem_swap_dict.keys():

                        month_year = datetime.datetime.strptime(key, "%Y-%m")
                        ws3_row += 1
                        # date_format = workbook.add_format({date_month: 'yyyy-mm'})
                        ws4.write(ws4_row, 0, month_year, format)

                        ws4.write(ws4_row, 1, float(mem_swap_dict[key][0]))
                        if len(mem_swap_dict[key]) == 2:
                            ws4.write(ws4_row, 2, float(mem_swap_dict[key][1]))
                        else:
                            ws4.write(ws4_row, 2, 0)
                        ws4_row +=1

                    chart = workbook.add_chart({'type': 'line'})
                    chart.set_x_axis({
                        'date_axis': True,
                        'name': 'Date'
                    })
                    chart.set_y_axis({
                        'name': 'Percentage',
                        'min': 0, 'max': 100
                    })
                    # chart.set_size({'width': 720, 'height': 288}) # default chart width x height is 480 x 288 pixels
                    chart.add_series({
                        'name': 'Memory',
                        'categories': ["mem_swap", i, 0, ws4_row-1, 0],
                        'values': ["mem_swap", i, 1, ws4_row-1, 1],
                        'marker': {'type': 'x'},

                    })
                    chart.set_title({
                        'name': 'Memory/Swap ',
                        'name_font': {
                            'name': 'Calibri'
                        }
                    })

                    chart.add_series({
                        'name': 'Swap',
                        'categories': ["mem_swap", i, 0, ws4_row - 1, 0],
                        'values': ["mem_swap", i, 2, ws4_row - 1, 2],
                        'marker': {'type': 'diamond'},

                    })
                    ws4_row += 1
                    worksheet.insert_chart('A' + str(row), chart)
                    row += 18


                worksheet.hide()
                ws2.hide()
                ws3.hide()
                ws4.hide()
                row += 2
            return "success", "success"
        except Exception as ex:
            print("Exception while writing xls file:  " + str(ex))
            return "Exception while writing xls file:  " + str(ex), "error"
