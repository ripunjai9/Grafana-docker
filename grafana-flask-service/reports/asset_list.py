from sciencelogic_db import ScienceLogicDb
from reports.separate_report_xls import SeparateReportXLs
from reports.report_utils import ReportUtility

utils = ReportUtility()
xls = SeparateReportXLs()


class AssetList:
    def __init__(self):
        self.sciencelogic_db = ScienceLogicDb()

    def get_report(self, from_date, to_date, organizations, devices_by_organization):
        xls_dict = {
            "asset_list": self.generate_report(organizations, devices_by_organization)
        }
        return xls.write_data_xls(xls_dict, from_date, to_date)

    def generate_report(self, organizations, devices_by_organization):
        query = utils.frame_query("asset_list")
        params = (organizations, devices_by_organization,)
        rows = self.sciencelogic_db.execute(query, params, True)
        group_data = self.group_data(rows)
        return group_data


    def group_data(self, rows):
        headers = rows[0]
        headers.pop(1)
        rows.pop(0)
        final_dict = {
            "report_headers": headers
        }
        for data in rows:
            event_messages = "Organization: "+str(data[1])
            if final_dict.get(event_messages) is None:
                data.pop(1)
                temp_list = [data]
                final_dict[event_messages] = temp_list
            else:
                data.pop(1)
                final_dict.get(event_messages).append(data)
        return final_dict
