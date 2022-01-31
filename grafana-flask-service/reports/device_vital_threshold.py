from reports.separate_report_xls import SeparateReportXLs
from reports.report_utils import ReportUtility
from sciencelogic_db import ScienceLogicDb

utils = ReportUtility()
xls = SeparateReportXLs()


class DeviceVitalThreshold:
    def __init__(self):
        self.sciencelogic_db = ScienceLogicDb()

    def get_report(
        self, from_date, to_date, organizations, devices_by_organization
    ):
        xls_dict = {
            "device_threshold": self.generate_report(
                from_date, to_date, organizations, devices_by_organization)
        }
        return xls.write_data_xls(xls_dict, from_date, to_date)

    def generate_report(
        self, from_date, to_date, organizations, devices_by_organization
    ):
        query = utils.frame_query("device_vital_threshold")
        headers = ['        Device          ']
        final_dict = {
            "report_headers": headers
        }
        final = {}
        count = 0
        for innser_query in query.split("===next==="):
            params = (
                organizations, devices_by_organization,
                from_date, to_date,)
            data = self.sciencelogic_db.execute(innser_query, params, True)
            headr = data[0]
            headr.pop(0)
            headr.pop(0)
            headers.extend(headr)
            data.pop(0)
            for v in data:
                name = v[1]
                if final.get(name) is None:
                    if count > 0:
                        for i in range(count):
                            v.insert(i+2, "")
                    final[name] = v
                else:
                    temp = [v[2]]
                    final.get(name).extend(temp)
            count += 1
        res_dict = self.group_data(final)
        final_dict.update(res_dict)
        return final_dict


    def group_data(self, result_dict):
        final_dict = {}
        for key, data in result_dict.items():
            event_messages = "Organization: " + str(data[0])
            if final_dict.get(event_messages) is None:
                data.pop(0)
                temp_list = [data]
                final_dict[event_messages] = temp_list
            else:
                data.pop(0)
                final_dict.get(event_messages).append(data)
        return final_dict
