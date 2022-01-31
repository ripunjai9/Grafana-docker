import pandas as pd
import numpy as np

from reports.report_utils import ReportUtility
from graphql.graphql_util import GraphQLUtil

utils = ReportUtility()
graphql_util = GraphQLUtil()


class GraphqlDrilldownData:

    def get_query(self, type, organization_name, infrastructure, video_endpoint, audio_endpoint):
        if type in "summary_of_all_devices_device_count_graphql":
            return self.all_device_count(organization_name)
        elif type in "summary_of_all_devices_alarm_count_graphql":
            return self.device_alarm_count(organization_name)
        elif type in "summary_of_all_device_down_count_graphql":
            return self.device_down_count(organization_name)
        elif type in "eventDevice_device_count_graphql":
            return self.device_count(organization_name)
        elif type in "eventDevice_problematic_devices_graphql":
            return self.problematic_devices(organization_name)

        else:
            return {}

    def all_device_count(self, organization_name):
        try:
            f = open(
                utils.get_dashboard_drilldown_gql_path(
                ) + "all_devices/device_count.gql",
                "r")
            query = str(f.read())
            variables = {
                "Org": organization_name,
                "TotalCount": 10
            }
            response = graphql_util.request_graphql_api(query, variables)

            total_count = response.get("data").get(
                "devices").get("pageInfo").get("matchCount")

            variables["TotalCount"] = int(total_count)
            response = graphql_util.request_graphql_api(query, variables)
            res = response.get("data").get("devices").get("edges")

            jn_df = pd.json_normalize(res)
            if "node.asset" in jn_df:
                jn_df = jn_df.drop("node.asset", axis=1)

            jn_df = jn_df.replace(np.nan, "")
            list_to_dict = jn_df.to_dict("records")

            return {"result": list_to_dict}
        except Exception as e:
            print(e)
            return {}

    def device_alarm_count(self, organization_name):
        try:
            f = open(
                utils.get_dashboard_drilldown_gql_path(
                ) + "all_devices/alarm_count.gql",
                "r")
            query = str(f.read())

            variables = {
                "Org": organization_name,
                "TotalCount": 11,
                "Severity": ["1", "2", "3", "4"]
            }
            response = graphql_util.request_graphql_api(query, variables)
            total_count = response.get("data").get(
                "devices").get("pageInfo").get("matchCount")

            variables["TotalCount"] = int(total_count)

            response = graphql_util.request_graphql_api(query, variables)
            res = response.get("data").get("devices").get("edges")

            nd2 = graphql_util.groupby_events(res)
            final = graphql_util.change_severity_num_to_string(
                nd2, "node.severity")
            final = graphql_util.unix_date_time_df(final, 'node.dateLast')
            # final['node.dateLast'] = pd.to_datetime(final['node.dateLast'], unit='s')
            final = final.replace(np.nan, "")
            to_dict = final.to_dict("records")

            return {"result": to_dict}
        except Exception as e:
            print(e)
            return {}

    def device_down_count(self, org_name):
        try:
            f = open(
                utils.get_dashboard_drilldown_gql_path()
                + "all_devices/down_count.gql",
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
            res = response.get("data").get("devices").get("edges")

            gb_result = graphql_util.groupby_events(res)

            final = graphql_util.change_severity_num_to_string(
                gb_result, "node.severity")
            final = graphql_util.unix_date_time_df(final, 'node.dateLast')

            final = final.replace(np.nan, "")
            to_dict = final.to_dict("records")
            return {"result": to_dict}
        except Exception as e:
            print(e)
            return {}

    def device_count(self, org_name):
        try:
            f = open(
                utils.get_dashboard_drilldown_gql_path()
                + "top_10/device_count.gql",
                "r")
            query = str(f.read())

            variables = {
                "Org": org_name,
                "TotalCount": 1,
                "Severity": ["1", "2", "3", "4"],
            }
            response = graphql_util.request_graphql_api(query, variables)
            total_count = response.get("data").get(
                "devices").get("pageInfo").get("matchCount")
            variables["TotalCount"] = int(total_count)

            response = graphql_util.request_graphql_api(query, variables)
            response = response.get("data").get("devices").get("edges")

            nd3 = graphql_util.groupby_events(response)
            gp_message_count = graphql_util.top_10_unique_problematic_name(
                response, "node.message")

            nd4 = pd.merge(
                gp_message_count, nd3,
                on='node.message', how='left')
            final = graphql_util.change_severity_num_to_string(
                nd4, "node.severity")
            # final['node.dateLast'] = pd.to_datetime(final['node.dateLast'], unit='s')
            final = graphql_util.unix_date_time_df(final, 'node.dateLast')

            final = final.replace(np.nan, "")
            to_dict = final.to_dict("records")
            return {"result": to_dict}
        except Exception as e:
            print(e)
            return {}

    def problematic_devices(self, org_name):
        try:
            f = open(
                utils.get_dashboard_drilldown_gql_path()
                + "top_10/problematic_devices.gql",
                "r")
            query = str(f.read())

            variables = {
                "Org": org_name,
                "TotalCount": 1,
                "Severity": ["1", "2", "3", "4"],
            }
            response = graphql_util.request_graphql_api(query, variables)
            total_count = response.get("data").get(
                "devices").get("pageInfo").get("matchCount")
            variables["TotalCount"] = int(total_count)

            response = graphql_util.request_graphql_api(query, variables)
            response = response.get("data").get("devices").get("edges")

            gp_message_count = graphql_util.top_10_unique_problematic_name(
                response=response, group_by_name="node.name")
            nd3 = graphql_util.groupby_events(response)
            nd4 = pd.merge(gp_message_count, nd3, on='node.name', how='left')

            final = graphql_util.change_severity_num_to_string(
                nd4, "node.severity")
            final = graphql_util.unix_date_time_df(final, 'node.dateLast')
            final = final.replace(np.nan, "")

            to_dict = final.to_dict("records")

            return {"result": to_dict}
        except Exception as e:
            print("error", e)
            return {}
