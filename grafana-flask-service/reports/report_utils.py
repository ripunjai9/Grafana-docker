import os
import random
import string
import datetime


class ReportUtility:

    def gen_random(self):
        keylist = [
            random.choice(string.ascii_letters + string.digits) for i in range(20)]
        return str(("".join(keylist)))

    def get_report_path(self):
        script_path = os.path.abspath(__file__)
        folder_path = os.path.split(script_path)
        return str(os.path.join(folder_path[0], 'saved_reports/'))

    def get_query_path(self):
        script_path = os.path.abspath(__file__)
        folder_path = os.path.split(script_path)
        return str(os.path.join(folder_path[0], 'sql/'))

    def get_poly_logo(self):
        script_path = os.path.abspath(__file__)
        folder_path = os.path.split(script_path)
        return str(os.path.join(folder_path[0], 'report_poly_logo/'))

    def get_query_dynamic_values(self, organization_name):
        if organization_name is None or len(organization_name) == 0:
            return ""
        org_query = "("
        if organization_name is not None and len(organization_name) > 0:
            for org in organization_name:
                org_query += "'"+str(org).strip()+"',"
            org_query = str(org_query[:-1])+")"
        return org_query

    def get_datetime(self, timestamp):
        if timestamp is None or len(timestamp) == 0:
            return ""
        date = datetime.datetime.fromtimestamp(int(timestamp) / 1e3)
        return str(date)[0:19]

    def getDateTime(self):
        from datetime import datetime
        now = datetime.now()
        dt_string = str(now.strftime("%d/%m/%Y"))
        return dt_string

    def get_dashboard_query_path(self):
        script_path = os.path.abspath(__file__)
        folder_path = os.path.split(script_path)
        return str(os.path.join(
            folder_path[0], "..", 'dashboard_report_queries/'))

    def get_drilldown_dashboard_query_path(self):
        script_path = os.path.abspath(__file__)
        folder_path = os.path.split(script_path)
        return str(os.path.join(
            folder_path[0], "..", 'drilldown_dashboard_data_query/'))

    def frame_query(self, filename):
        f = open(self.get_query_path() + str(filename)+".sql", "r")
        sql = f.read()
        return sql
