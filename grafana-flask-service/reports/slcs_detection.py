from reports.separate_report_xls import SeparateReportXLs
from reports.report_utils import ReportUtility
from sciencelogic_db import ScienceLogicDb

utils = ReportUtility()
xls = SeparateReportXLs()


class SlcsDetection:
    def __init__(self):
        self.sciencelogic_db = ScienceLogicDb()

    def get_report(
        self, from_date, to_date, organizations, devices_by_organization
    ):

        xls_dict = {
            "scls_detection": self.generate_report(
                from_date, to_date, organizations, devices_by_organization)
        }
        return xls.write_data_xls(xls_dict, from_date, to_date)

    def generate_report(
        self, from_date, to_date, organizations, devices_by_organization
    ):
        query = utils.frame_query("slcs_events")
        params = (organizations, devices_by_organization, from_date, to_date)
        results = self.sciencelogic_db.execute(query, params, True)
        result_dict = self.group_data(results)
        return result_dict

    def group_data(self, rows):
        headers = rows[0]
        headers.pop(0)
        rows.pop(0)
        final_dict = {
            "report_headers": headers
        }
        for data in rows:
            event_messages = "Event: "+str(data[0])
            if final_dict.get(event_messages) is None:
                data.pop(0)
                temp_list = [data]
                final_dict[event_messages] = temp_list
            else:
                data.pop(0)
                final_dict.get(event_messages).append(data)
        return final_dict
