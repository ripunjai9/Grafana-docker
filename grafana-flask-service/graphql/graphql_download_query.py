import pandas as pd

from xls_writer import XlsWriter
from graphql.graphql_util import GraphQLUtil
from graphql.graphql_util import GraphQLUtil

utils = GraphQLUtil()
graphql_util = GraphQLUtil()
xls = XlsWriter()

gql_url = "http://10.6.82.231/gql"
gql_username = "em7admin"
gql_password = "Polycom123"

event_headers = [
    'node.name', 'node.organization.OrganizationName', 'node.IP',
    'node.deviceClass.DeviceClassSubClass',
    'node.deviceClass.deviceCategory.DeviceCategory',
    'node.asset.Location', 'node.asset.vendor',
    'node.Message', 'node.severity', 'node.LastDetection']

device_headers = [
    'node.name', 'node.organization.OrganizationName', 'node.IP',
    'node.deviceClass.DeviceClassSubClass',
    'node.deviceClass.deviceCategory.DeviceCategory',
    'node.asset.Location', 'node.asset.vendor']


class GraphqlDownloadData:

    def get_query(
        self, type, organization_name, infrastructure, video_endpoint, audio_endpoint
    ):

        if type in "summary_of_all_devices_graphql":
            return self.summary_of_all_devices(organization_name)
        elif type in "eventDevice_device_count_graphql":
            return self.device_count(organization_name)
        elif type in "eventDevice_problematic_devices_graphql":
            return self.problematic_devices(organization_name)

        else:
            return {}

    def summary_of_all_devices(self, organization_name):
        try:
            f = open(
                utils.get_dashboard_download_gql_path() +
                "all_devices_summary.gql", "r")
            query = str(f.read())
            variables = {
                "Org": organization_name,
                "Severity": ["1", "2", "3", "4"],
                "TotalCount": 7
            }
            response = graphql_util.request_graphql_api(query, variables)
            total_count = response.get("data").get(
                "TotalDeviceSummary").get("pageInfo").get("matchCount")
            variables["TotalCount"] = total_count

            response = graphql_util.request_graphql_api(query, variables)
            total_device_summary_response = response.get(
                "data").get("TotalDeviceSummary").get("edges")
            total_device_summary = self.all_devices_count(
                total_device_summary_response)

            device_alarm_summary_response = response.get(
                "data").get("DeviceAlarmSummary").get("edges")
            device_alarm_summary = self.all_devices_alarm_count(
                device_alarm_summary_response)

            device_down_count_summary_response = response.get(
                "data").get("DeviceDownCountSummary").get("edges")
            device_down_count_summary = self.all_devices_down_count(
                device_down_count_summary_response)

            xls_dict = {
                "total_device_summary": total_device_summary,
                "device_alarm_summary": device_alarm_summary,
                "device_down_count_summary": device_down_count_summary
            }
            file_name = xls.write_data_xls(xls_dict)
            return file_name
        except Exception as e:
            print(e)
            return {}

    def all_devices_count(self, response):
        try:
            jn_df = pd.json_normalize(response)
            jn_df = jn_df[device_headers]
            list_to_dict = jn_df.values.tolist()
            header = (list(jn_df.columns.values.tolist()))
            header = graphql_util.lastWord(header)
            list_to_dict.insert(0, header)

            return list_to_dict
        except Exception as e:
            print(e)
            return {}

    def all_devices_alarm_count(self, response):
        try:
            nd2 = graphql_util.groupby_events(response)
            nd2 = nd2[event_headers]
            final = graphql_util.change_severity_num_to_string(
                nd2, "node.severity")
            final = graphql_util.unix_date_time_df(final, 'node.LastDetection')

            # to_dict = final.to_dict("records")
            list_to_dict = final.values.tolist()
            header = (list(final.columns.values.tolist()))
            header = graphql_util.lastWord(header)
            list_to_dict.insert(0, header)
            # print(list_to_dict)
            return list_to_dict
        except Exception as e:
            print(e)
            return {}

    def all_devices_down_count(self, response):
        try:
            gb_result = graphql_util.groupby_events(response)
            final = graphql_util.change_severity_num_to_string(
                gb_result, "node.severity")
            final = graphql_util.unix_date_time_df(final, 'node.LastDetection')
            final = final[event_headers]

            list_to_dict = final.values.tolist()
            header = (list(final.columns.values.tolist()))
            header = graphql_util.lastWord(header)
            list_to_dict.insert(0, header)
            return list_to_dict
        except Exception as e:
            print(e)
            return {}

    def device_count(self, org_name):
        try:
            f = open(
                utils.get_dashboard_download_gql_path()
                + "top_10/device_count.gql",
                "r")
            query = str(f.read())

            variables = {
                "Org": org_name,
                "TotalCount": 5,
                "Severity": ["1", "2", "3", "4"]
            }
            response = graphql_util.request_graphql_api(query, variables)
            total_count = response.get("data").get(
                "devices").get("pageInfo").get("matchCount")
            variables["TotalCount"] = int(total_count)

            response = graphql_util.request_graphql_api(query, variables)
            response = response.get("data").get("devices").get("edges")

            gp_message_count = graphql_util.top_10_unique_problematic_name(
                response, "node.Message")
            nd3 = graphql_util.groupby_events(response)
            nd4 = pd.merge(
                nd3, gp_message_count,
                on='node.Message', how='right')

            nd4 = nd4[event_headers]
            final = graphql_util.change_severity_num_to_string(
                nd4, "node.severity")
            final = graphql_util.unix_date_time_df(final, 'node.LastDetection')

            list_to_dict = final.values.tolist()
            header = (list(final.columns.values.tolist()))
            header = graphql_util.lastWord(header)
            list_to_dict.insert(0, header)
            xls_dict = {"Device_Events": list_to_dict}
            file_name = xls.write_data_xls(xls_dict)
            return file_name
        except Exception as e:
            print(e)
            return {}

    def problematic_devices(self, org_name):
        try:
            f = open(
                utils.get_dashboard_download_gql_path()
                + "top_10/problematic_devices.gql",
                "r")
            query = str(f.read())

            variables = {
                "Org": org_name,
                "TotalCount": 1,
            }
            response = graphql_util.request_graphql_api(query, variables)
            total_count = response.get("data").get(
                "devices").get("pageInfo").get("matchCount")
            variables["TotalCount"] = int(total_count)

            response = graphql_util.request_graphql_api(query, variables)
            response = response.get("data").get("devices").get("edges")

            gp_message_count = graphql_util.top_10_unique_problematic_name(
                response, "node.name")
            nd3 = graphql_util.groupby_events(response)
            final = pd.merge(gp_message_count, nd3, on='node.name', how='left')
            final = final[event_headers]
            final_sev = graphql_util.change_severity_num_to_string(
                final, "node.severity")
            final_lastDate = graphql_util.unix_date_time_df(
                final_sev, 'node.LastDetection')

            # DataFrame to list of list
            list_to_dict = final_lastDate.values.tolist()
            # get the header of the DataFrame
            header = (list(final_lastDate.columns.values.tolist()))
            header = graphql_util.lastWord(header)
            # insert the modified header in the list
            list_to_dict.insert(0, header)

            xls_dict = {"Problematic_Devices": list_to_dict}
            file_name = xls.write_data_xls(xls_dict)
            return file_name
        except Exception as e:
            print(e)
            return {}
