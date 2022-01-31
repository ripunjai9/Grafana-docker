from reports.report_utils import ReportUtility
from sciencelogic_db import ScienceLogicDb
import xlsxwriter
from datetime import datetime
import datetime

utils = ReportUtility()


class UniqueEvents:
    def __init__(self):
        self.sciencelogic_db = ScienceLogicDb()
	
    def get_report(self, from_date, to_date, organizations, devices_by_organization):
        final_list, headers =self.frame_query(from_date, to_date, organizations, devices_by_organization)
        sheet_name = "Unique_Events"
        return self.write_data_xls(final_list, headers, sheet_name ,from_date, to_date)

    def frame_query(self, from_date, to_date, organizations, devices_by_organization):
        f = open(utils.get_query_path() + "unique_events.sql", "r")
        time_duration_list = self.get_date_list(from_date, to_date)
        query_text = str(f.read())
        headers = ['    Event Message                         ']
        event_dict = {}
        date_dict = {}
        for duration_tim in time_duration_list:
            repprt_date = "'"+str(duration_tim.replace("'",""))+"'"
            final_query = str(query_text).replace("($duration)",duration_tim).replace("$date_time",repprt_date)
            params = (organizations, devices_by_organization)
            result = self.sciencelogic_db.execute(final_query, params, True)
            result.pop(0)
            headers.append(str(duration_tim.replace("AND","TO")))
            if result is not None and len(result) > 0:
                for res in result:
                    event_message = res[0]
                    dict_time = res[2]
                    if event_dict.get(event_message) is None:
                        temp_dict = [res]
                        event_dict[event_message] = temp_dict
                    else:
                        event_dict.get(event_message).append(res)

                    if date_dict.get(dict_time) is None:
                        temp_dict = [res]
                        date_dict[dict_time] = temp_dict
                    else:
                        date_dict.get(dict_time).append(res)


        final_list = []
        for key, value in event_dict.items():
            temp_list = [key]
            for dt, vl in date_dict.items():
                flag = True
                count =0
                for i in vl:
                    if key == i[0]:
                        flag = False
                        temp_list.append(i[1])
                if flag:
                    temp_list.append(0)
            total_list = temp_list[1:]
            total = 0
            for t in total_list:
                total += int(t)
            temp_list.append(total)
            final_list.append(temp_list)
        headers.append('    total     ')
        return final_list, headers

    def get_date_list(self, startDate, endDate):
        from datetime import datetime
        from dateutil import relativedelta
        date1 = datetime.strptime(str(startDate), '%Y-%m-%d %H:%M:%S')
        date2 = datetime.strptime(str(endDate), '%Y-%m-%d %H:%M:%S')
        r = relativedelta.relativedelta(date2, date1)
        date_list = []
        if r.months > 0:
            date_list.append("'" + startDate + "' AND '" + self.get_last_month(str(startDate[:10])) + " 23:59:59'")
            from datetime import datetime
            from dateutil.relativedelta import relativedelta
            cur_date = datetime.strptime(startDate, '%Y-%m-%d %H:%M:%S').date()
            end = datetime.strptime(endDate, '%Y-%m-%d %H:%M:%S').date()
            while cur_date < end:
                date_list.append(
                    "'" + str(cur_date) + " 00:00:00" + "' AND '" + self.get_last_month(str(cur_date)) + " 23:59:59'")
                cur_date += relativedelta(months=1)
            date_list.pop(1)
            last_date = str(date_list[len(date_list) - 1]).split('AND')
            date_list.pop(len(date_list) - 1)
            date_list.append(str(last_date[0]) + "AND '" + endDate + "'")
        else:
            date_list.append("'" + startDate + "' AND '" + endDate + "'")
        return date_list

    def get_last_month(self, str_date):
        from dateutil.relativedelta import relativedelta
        from datetime import datetime
        mydate = datetime.strptime(str(str_date), '%Y-%m-%d')
        last_date_of_month = datetime(mydate.year, mydate.month, 1) + relativedelta(months=1, days=-1)
        return str(last_date_of_month)

    def write_data_xls(self, final_list, headers, sheet_name ,from_date, to_date):
        x = datetime.datetime.now()
        date_time_str = x.strftime("%d_%m_%YT%H_%M_%S")
        file_name = "xls_data_" + utils.gen_random() + str(date_time_str + ".xlsx")
        workbook = xlsxwriter.Workbook(str(utils.get_report_path()) + file_name)
        self.write_query_records(workbook, final_list,headers, sheet_name, from_date, to_date)
        workbook.close()
        return file_name

    def write_query_records(self, workbook, final_list,headers, sheet_name, from_date, to_date):
        try:
            header_list = headers
            worksheet = workbook.add_worksheet(sheet_name)
            worksheet.merge_range('A1:D3', "")
            worksheet.write('H1', "Generated on: " + str(utils.getDateTime()))
            worksheet.write('H2', "Begin: " + str(from_date))
            worksheet.write('H3', "End: " + str(to_date))
            header_format = workbook.add_format({'bold': True, 'bg_color': '#e6e6e6', "align": "center"})
            event_format = workbook.add_format({'bold': True, 'bg_color': '#999999'})
            # worksheet.insert_image('A1', utils.get_poly_logo() + 'poly_report_logo.JPG', {'x_scale': 0.3, 'y_scale': 0.2})
            worksheet.insert_image('A1', utils.get_poly_logo() + 'poly_report_logo.jpg', {'x_scale': 1, 'y_scale': 0.8})
            row = 5
            column = 0
            row += 1
            for header in header_list:
                width = len(str(header)) + 2
                worksheet.set_column(row, column, width)
                worksheet.write(row, column, header, header_format)
                column += 1
            row += 1
            if len(final_list) > 0:
                    for rows in final_list:
                        d_column = 0
                        for dt in rows:
                            
                            worksheet.write(row, d_column, dt)
                            d_column += 1
                        row += 1
            else:
                worksheet.merge_range("A" + str(row + 1) + ":F" + str(row + 1) + "", str("No Data Found"), event_format)
            return "success", "success"
        except Exception as ex:
            print("Exception while writing xls file:  " + str(ex))
            return "Exception while writing xls file:  " + str(ex), "error"

