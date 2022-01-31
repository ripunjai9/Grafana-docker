from reports.separate_report_xls import SeparateReportXLs
from reports.report_utils import ReportUtility
from sciencelogic_db import ScienceLogicDb


utils = ReportUtility()
xls = SeparateReportXLs()


class DeviceAvailability:
    def __init__(self):
        self.sciencelogic_db = ScienceLogicDb()

    def get_report(self, from_date, to_date, organizations, devices_by_organization):
        xls_dict = {
            "Device Availability": self.generate_report(from_date, to_date, organizations, devices_by_organization)
        }
        return xls.write_data_xls(xls_dict, from_date, to_date)

    def generate_report(self, from_date, to_date, organizations, devices_by_organization):
        query = self.frame_query(from_date, to_date, organizations, devices_by_organization)
        params = ( organizations, devices_by_organization, from_date, to_date, )
        results = self.sciencelogic_db.execute(query, params, True)
        result_dict = self.group_data(results)
        return result_dict

    def frame_query(self, from_date, to_date, organizations, devices_by_organization):
        f = open(utils.get_query_path() + "device_availability.sql", "r")
        query_text = f.read()
        date_diff = self.diff_dates(from_date, to_date)
        final_query = str(query_text).replace("$Durationtime", str(date_diff))
        return final_query

    def group_data(self, rows):
        headers = rows[0]
        headers.pop(0)
        rows.pop(0)
        final_dict = {
            "report_headers": headers
        }
        for data in rows:
            event_messages = "Organization: " + str(data[0])
            downtime = self.seconds_to_human_readable(data[4])
            data[4] = downtime
            uptime = self.seconds_to_human_readable(data[6])
            data[6] = uptime
            if final_dict.get(event_messages) is None:
                data.pop(0)
                temp_list = [data]
                final_dict[event_messages] = temp_list
            else:
                data.pop(0)
                final_dict.get(event_messages).append(data)
        return final_dict

    def diff_dates(self, d1, d2):
        import time
        # Date format: %Y-%m-%d %H:%M:%S
        return (time.mktime(time.strptime(d2, "%Y-%m-%d %H:%M:%S")) -
                time.mktime(time.strptime(d1, "%Y-%m-%d %H:%M:%S")))

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
