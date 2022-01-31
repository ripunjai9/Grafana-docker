from reports.report_xls import ReportXls
from reports.report_utils import ReportUtility
from sciencelogic_db import ScienceLogicDb

utils = ReportUtility()
xls = ReportXls()


class EventDetection:
    def __init__(self):
        self.sciencelogic_db = ScienceLogicDb()

    def get_report(self, from_date, to_date, organizations, devices_by_organization):
        xls_dict = {
            "event_detection": self.generate_report(
                from_date, to_date, organizations, devices_by_organization)
        }
        return xls.write_data_xls(xls_dict, from_date, to_date)

    def generate_report(self, from_date, to_date, organizations, devices_by_organization):
        query = utils.frame_query("event_detection")
        params = (
            organizations, devices_by_organization,
            from_date, to_date,
            organizations, devices_by_organization,
            from_date, to_date,)

        results = self.sciencelogic_db.execute(query, params, True)
        return results


    def group_data(self, rows):
        headers = rows[0]
        headers.pop(2)
        rows.pop(0)
        final_dict = {
            "report_headers": headers
        }
        for data in rows:
            event_messages = "Event: " + str(data[2])
            if final_dict.get(event_messages) is None:
                data.pop(2)
                temp_list = [data]
                final_dict[event_messages] = temp_list
            else:
                data.pop(2)
                final_dict.get(event_messages).append(data)
        return final_dict
