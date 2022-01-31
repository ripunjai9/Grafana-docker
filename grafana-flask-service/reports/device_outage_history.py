from reports.separate_report_xls import SeparateReportXLs
from reports.report_utils import ReportUtility
from sciencelogic_db import ScienceLogicDb

utils = ReportUtility()
xls = SeparateReportXLs()


class DeviceOutageHistory:
    def __init__(self):
        self.sciencelogic_db = ScienceLogicDb()

    def get_report(
        self, from_date, to_date, organizations, devices_by_organization
    ):
        xls_dict = {
            "outage_history": self.generate_report(
                from_date, to_date, organizations, devices_by_organization)
        }
        return xls.write_data_xls(xls_dict, from_date, to_date)

    def generate_report(
        self, from_date, to_date, organizations, devices_by_organization
    ):
        query_list = utils.frame_query("outage_history")
        query = query_list.split("===next===")
        params = (organizations, devices_by_organization, from_date, to_date)
        rows = self.sciencelogic_db.execute(query[0], params, True)
        headers = {
            "report_headers": [
                '              Device Name                  ',
                '                  Outage Start                  ',
                '                  Outage End                  ',
                '                  Downtime                  '
            ]
        }
        rows.pop(0)
        result_dict = self.filter_results(rows)
        result_still_down = self.sciencelogic_db.execute(
            query[1], params, True)
        result_still_down.pop(0)
        final_dict = self.group_data(result_still_down, result_dict)
        final_dict.update(headers)
        return result_dict

    def filter_results(self, results):
        group_by_device = {}
        for data in results:
            device_id = str(data[2])
            if group_by_device.get(device_id) is None:
                temp_list = [data]
                group_by_device[device_id] = temp_list
            else:
                group_by_device.get(device_id).append(data)

        for key, value in group_by_device.items():
            duplicate_record = {}
            lenhh = len(value)
            if lenhh % 2 != 0:
                v1 = value[0][3]
                v2 = value[len(value) - 1][3]
                if v1 == 268:
                    value.pop(0)
                elif v2 == 267:
                    value.pop(len(value) - 1)
            for v in value:
                kk = str(v[1]) + str(v[5])
                if duplicate_record.get(kk) is None:
                    duplicate_record[kk] = ""
                else:
                    value.remove(v)
        final_dict = {}
        for key, value in group_by_device.items():
            record_first = 0
            record_last = 1
            value_range = len(value)-1
            for i in range(0, value_range):
                if record_last == len(value)-1:
                    break
                from datetime import datetime
                dt1 = datetime.strptime(
                    str(value[record_last][5]), '%Y-%m-%d %H:%M:%S')
                dt2 = datetime.strptime(
                    str(value[record_first][5]), '%Y-%m-%d %H:%M:%S')
                duration_in_s = (dt1 - dt2).total_seconds()
                days = divmod(duration_in_s, 86400)  # Get days (without [0]!)
                # Use remainder of days to calc hours
                hours = divmod(days[1], 3600)
                # Use remainder of hours to calc minutes
                minutes = divmod(hours[1], 60)
                # Use remainder of minutes to calc seconds
                seconds = divmod(minutes[1], 1)
                downtime = " %d days, %d hours, %d minutes and %d seconds" % (
                    days[0], hours[0], minutes[0], seconds[0])
                org = "Organization: "+str(value[record_first][0])
                device_name = value[record_first][1]
                start_date = value[record_first][5]
                end_date = value[record_last][5]
                if final_dict.get(org) is None:
                    temp_list = [[device_name, start_date, end_date, downtime]]
                    final_dict[org] = temp_list
                else:
                    temp_list = [device_name, start_date, end_date, downtime]
                    final_dict.get(org).append(temp_list)
                record_first += 1
                record_last += 1
        return final_dict

    def group_data(self, results, final_dict):
        for data in results:
            event_messages = "Organization: "+str(data[0])
            if final_dict.get(event_messages) is None:
                data.pop(0)
                temp_list = [data]
                final_dict[event_messages] = temp_list
            else:
                data.pop(0)
                final_dict.get(event_messages).append(data)
        return final_dict
