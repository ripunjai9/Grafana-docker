from reports.separate_report_xls import SeparateReportXLs
from sciencelogic_db import ScienceLogicDb
from reports.report_utils import ReportUtility

utils = ReportUtility()
xls = SeparateReportXLs()


class DeviceUptime:
    def __init__(self):
        self.sciencelogic_db = ScienceLogicDb()

    def get_report(self, from_date, to_date, organizations, devices_by_organization):
        xls_dict = {
            "Device_Uptime": self.generate_report(from_date, to_date, organizations, devices_by_organization)
        }
        return xls.write_data_xls(xls_dict, from_date, to_date)

    def generate_report(self, from_date, to_date, organizations, devices_by_organization):
        query = utils.frame_query("device_uptime")
        params = (organizations, devices_by_organization,)
        results = self.sciencelogic_db.execute(query, params, True)
        result_dict = self.group_data(results)
        return result_dict


    def group_data(self, rows):
        headers = rows[0]
        headers.pop(5)
        headers.pop(0)
        rows.pop(0)
        final_headers = []
        for h in headers:
            final_headers.append(str("         ")+h+str("               "))
        final_dict = {
            "report_headers": final_headers
        }
        for data in rows:
            event_messages = "Organization: "+str(data[0])
            uptime = str(data[4])
            if 'down' not in uptime:
                data[4] = self.seconds_to_human_readable(uptime)
            timetick = str(data[5])
            if timetick is not None and len(str(timetick)) > 0:
                from datetime import datetime
                last_polled = datetime.strptime(
                    str(data[7]), '%Y-%m-%d %H:%M:%S')
                import datetime
                data[6] = str(
                    last_polled - datetime.timedelta(seconds=int(float(uptime))))
            if final_dict.get(event_messages) is None:
                data.pop(5)
                data.pop(0)
                temp_list = [data]
                final_dict[event_messages] = temp_list
            else:
                data.pop(5)
                data.pop(0)
                final_dict.get(event_messages).append(data)

        return final_dict

    def seconds_to_human_readable(self, seconds):
        seconds = int(float(seconds))
        weeks, seconds = divmod(seconds, 7 * 24 * 60 * 60)
        days, seconds = divmod(seconds, 24 * 60 * 60)
        hours, seconds = divmod(seconds, 60 * 60)
        minutes, seconds = divmod(seconds, 60)
        final_string = ""
        if weeks > 0:
            final_string += str(weeks) + " weeks "
        if days > 0:
            final_string += str(days) + " days "
        if hours > 0:
            final_string += str(hours) + " hours "
        if minutes > 0:
            final_string += str(minutes) + " minutes "
        if seconds > 0:
            final_string += str(seconds) + " seconds "
        return final_string
