from datetime import datetime
import configparser
import requests
import pandas as pd
import json
import os
from requests.auth import HTTPBasicAuth
from imp import reload


class GraphQLUtil:
    # Request GET graphql Module
    def request_graphql_api(self, query, variables):
        try:
            connection_data = self.read_graphql_property_file()
            gql_url = connection_data.get("gql_url")
            gql_username = connection_data.get("gql_username")
            gql_password = connection_data.get("gql_password")

            payload = json.dumps({
                "query": query,
                "variables": variables
            })

            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.request(
                "GET", gql_url, headers=headers, data=payload,
                auth=HTTPBasicAuth(gql_username, gql_password),
                verify=False)
            response = response.json()

            return response
        except Exception as e:
            print(e)
            return {}

    # Change the number of severity to Sting in the DataFrame
    def change_severity_num_to_string(self, df, severity):
        severity_list = {
            "0": 'Healthy',
            "1": 'Notify',
            "2": 'Minor',
            "3": 'Major',
            "4": 'Critical'
        }
        df[severity] = df[severity].replace(severity_list)
        return df

    def unix_date_time_df(self, df, fied_name):
        try:
            df[fied_name] = df[fied_name].apply(
                lambda x: self.unix_date_time(x))
            return df
        except Exception as E:
            print("unix_date_time_df error: ", E)

    def unix_date_time(self, _unix_time):
        try:
            _date_time = datetime.fromtimestamp(
                int(_unix_time)).strftime('%Y-%m-%d %H:%M:%S')

            return str(_date_time)
        except Exception as E:
            print("error: ", E)

    def groupby_events(self, res):
        try:
            nd1 = pd.json_normalize(
                res, record_path=["node", "events", "edges"],
                meta=[["node", "id"]])
            nd = pd.json_normalize(res)
            nd = nd.drop("node.events.edges", axis=1)

            nd2 = pd.merge(nd1, nd, on='node.id', how='left')
            nd2.drop("node.id", axis=1)
            return nd2
        except Exception as e:
            print(e)
            return {}

    def top_10_unique_problematic_name(self, response, group_by_name):
        try:
            df_json = pd.json_normalize(
                response,
                record_path=["node", "events", "edges"],
                meta=[["node", "name"]])
            gp_message_count1 = df_json.groupby([str(group_by_name)])\
                .size().reset_index(name='counts')\
                .sort_values("counts", ascending=False).head(10)
            gp_message_count = gp_message_count1.drop("counts", axis=1)
            return gp_message_count
        except Exception as e:
            print(e)
            return {}

    @staticmethod
    def lastWord(list_string):
        """
        from list of the field([node.name, node.ip]) get the last name([name, ip]) 
        """
        try:
            list_last_word = []
            for word in list_string:
                lis = list(word.split("."))
                last_word = lis[-1]
                if not last_word[0].isupper():
                    last_word = last_word.capitalize()
                list_last_word.append(last_word)
            # returning replace words in list
            return list_last_word
        except Exception as e:
            print(e)
            return list_string

    def read_graphql_property_file(self):
        script_path = os.path.abspath(__file__)
        folder_path = os.path.split(script_path)
        properties_path = str(os.path.join(folder_path[0]))

        reload(configparser)
        config = configparser.RawConfigParser()
        config.read(properties_path + '/graph_ql.properties')
        return dict(config.items('grphQL_Connections'))

    def get_dashboard_gql_path(self):
        script_path = os.path.abspath(__file__)
        folder_path = os.path.split(script_path)
        return str(os.path.join(
            folder_path[0], "gql", 'dashboard/'))

    def get_dashboard_drilldown_gql_path(self):
        script_path = os.path.abspath(__file__)
        folder_path = os.path.split(script_path)
        return str(os.path.join(
            folder_path[0], "gql", 'dashboard_drilldown/'
        ))

    def get_dashboard_download_gql_path(self):
        script_path = os.path.abspath(__file__)
        folder_path = os.path.split(script_path)
        return str(os.path.join(
            folder_path[0], "gql", 'dashboard_download/'))
