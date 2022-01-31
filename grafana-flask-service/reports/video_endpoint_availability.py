from reports.separate_report_xls import SeparateReportXLs
from sciencelogic_db import ScienceLogicDb
from reports.report_utils import ReportUtility

utils = ReportUtility()
xls = SeparateReportXLs()


class VideoEndpointAvailability:
    def __init__(self):
        self.sciencelogic_db = ScienceLogicDb()
        
    def get_report(self, from_date,to_date,organizations,devices_by_organization):
        xls_dict = {
            "Video_Endpoint_Avail": self.generate_report(from_date, to_date, organizations, devices_by_organization )
        }
        return xls.write_data_xls(xls_dict, from_date,to_date)

    def generate_report(self, from_date, to_date, organizations, devices_by_organization):
        query = utils.frame_query("video_endpoint_availlability")
        params = (organizations, devices_by_organization, from_date, to_date, )
        results = self.sciencelogic_db.execute(query, params, True)
        result_dict = self.group_data(results)
        return result_dict

    def group_data(self, rows):
        headers = rows[0]
        headers.pop(3)
        rows.pop(0)
        final_dict = {
            "report_headers": headers
        }
        for data in rows:
            event_messages = "Device: " + str(data[3])
            if final_dict.get(event_messages) is None:
                data.pop(3)
                temp_list = [data]
                final_dict[event_messages] = temp_list
            else:
                data.pop(3)
                final_dict.get(event_messages).append(data)
        return final_dict