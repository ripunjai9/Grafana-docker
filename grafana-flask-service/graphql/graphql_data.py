from datetime import datetime
import pandas as pd

from graphql.graphql_util import GraphQLUtil

utility = GraphQLUtil()

severity = ["1", "2", "3", "4"]


class GraphqlData:

    def get_query(
        self, type, organization_name, infrastructure, video_endpoint, audio_endpoint
    ):

        if type in "summary_of_all_devices_device_count_graphql":
            return self.all_devices_count(organization_name)
        elif type in "summary_of_all_devices_alarm_count_graphql":
            return self.devices_alarm_count(organization_name)
        elif type in "summary_of_all_device_alarm_details_graphql":
            return self.devices_alarm_details(organization_name)
        elif type in "summary_of_all_devices_down_count_graphql":
            return self.devices_down_count(organization_name)
        elif type in "eventDevice_device_count_graphql":
            return self.device_count(organization_name)
        elif type in "eventDevice_problematic_devices_graphql":
            return self.problematic_devices(organization_name)
        else:
            return {}

    def all_devices_count(self, organizations):
        try:
            f = open(
                utility.get_dashboard_gql_path() +
                "all_devices/device_count.gql", "r")
            query = str(f.read())

            variables = {
                "Org": organizations
            }
            response = utility.request_graphql_api(query, variables)

            return {
                "result": response.get("data").get("devices").get("pageInfo").get("matchCount")
            }
        except Exception as e:
            print(e)
            return {}

    def devices_alarm_count(self, organization_name):
        try:
            f = open(
                utility.get_dashboard_gql_path() +
                "all_devices/alarm_count.gql", "r")
            query = str(f.read())

            variables = {
                "Org": organization_name,
                "Severity": ["1", "2", "3", "4"]
            }
            response = utility.request_graphql_api(query, variables)

            return {
                "result": response.get("data").get("events").get("pageInfo").get("matchCount")
            }

        except Exception as e:
            print(e)
            return {}

    def devices_alarm_details(self, organization_name):
        try:
            f = open(
                utility.get_dashboard_gql_path() +
                "all_devices/alarm_details.gql", "r")
            query = str(f.read())

            variables = {
                "Org": organization_name,
                "Severity": ["1", "2", "3", "4"]
            }
            response = utility.request_graphql_api(query, variables)

            return {
                "Critical": response.get("data").get("critical").get("pageInfo").get("matchCount"),
                "Major": response.get("data").get("major").get("pageInfo").get("matchCount"),
                "Minor": response.get("data").get("minor").get("pageInfo").get("matchCount"),
                "Notice": response.get("data").get("notice").get("pageInfo").get("matchCount"),
            }

        except Exception as e:
            print(e)
            return {}

    def devices_down_count(self, organization_name):
        try:
            f = open(
                utility.get_dashboard_gql_path() +
                "all_devices/down_count.gql", "r")
            query = str(f.read())

            variables = {
                "Org": organization_name  # ["CMC", "System"]
            }
            response = utility.request_graphql_api(query, variables)
            return {
                "Down Count": response.get("data").get("devices").get("pageInfo").get("matchCount")
            }

        except Exception as e:
            print(e)
            return {}

    def device_count(self, organization_name):
        try:
            f = open(
                utility.get_dashboard_gql_path() +
                "top_10/device_count.gql", "r")
            query = str(f.read())
            variables = {
                "Org": organization_name,  # ["CMC", "System"]
                "TotalCount": 10,
                "Severity": severity
            }

            response = utility.request_graphql_api(query, variables)
            total_count = response.get("data").get(
                "devices").get("pageInfo").get("matchCount")

            variables["TotalCount"] = total_count
            response = utility.request_graphql_api(query, variables)
            response = response.get("data").get("devices").get("edges")

            df_json = pd.json_normalize(
                response, record_path=["node", "events", "edges"],
                meta=[["node", "name"]])
            gp_name_count = df_json.groupby(["node.message"])\
                .size().reset_index(name='counts')\
                .sort_values("counts", ascending=False).head(10)
            # gp_name_count['node.dateLast'] = pd.to_datetime(gp_name_count['node.dateLast'], unit='s')
            gp_name_count['node.dateLast'] = pd.to_datetime(datetime.now())
            # change the length of the message
            gp_name_count["node.message"] = gp_name_count["node.message"]\
                .apply(lambda x: x[0:50])

            df_to_dict = gp_name_count.to_dict("records")

            final_dict = {"result": df_to_dict}
            count = len(df_to_dict)

            if count < 10:
                star = 1
                while True:
                    if count == 10:
                        break
                    star_string = ""
                    for i in range(0, star):
                        star_string += "."
                    temp_dict = {
                        "node.dateLast": "-1",
                        "node.message": star_string,
                        "counts": "0"
                    }
                    count += 1
                    star += 1
                    final_dict.get("result").append(temp_dict)

            return final_dict

        except Exception as e:
            print(e)
            return {}

    def problematic_devices(self, organization_name):
        try:
            f = open(
                utility.get_dashboard_gql_path() +
                "top_10/problematic_devices.gql", "r")
            query = str(f.read())

            variables = {
                "Org": organization_name,
                "TotalCount": 1,
                "Severity": severity

            }
            response = utility.request_graphql_api(query, variables)
            total_count = response.get("data").get(
                "devices").get("pageInfo").get("matchCount")

            variables["TotalCount"] = total_count
            response = utility.request_graphql_api(query, variables)
            response = response.get("data").get("devices").get("edges")

            df_json = pd.json_normalize(
                response, record_path=["node", "events", "edges"],
                meta=[["node", "name"]])
            gp_message_count = df_json.groupby(["node.name"])\
                .size().reset_index(name='counts')\
                .sort_values("counts", ascending=False).head(10)
            gp_message_count['node.dateLast'] = pd.to_datetime(datetime.now())

            df_to_dict = gp_message_count.to_dict("records")

            final_dict = {"result": df_to_dict}
            count = len(df_to_dict)
            if count < 10:
                while True:
                    if count == 10:
                        break
                    temp_dict = {
                        "node.dateLast": "-1",
                        "node.name": ".",
                        "counts": "0"
                    }
                    count += 1
                    final_dict.get("result").append(temp_dict)

            return final_dict
        except Exception as e:
            print(e)
            return {}
