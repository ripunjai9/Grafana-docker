import os
import configparser
from dotenv.main import dotenv_values


class Helpers:
    def __init__(self):
        self.ini_config = None
        self.__load_ini()

    def get_env_path(self):
        try:
            script_path = os.path.abspath(__file__)
            folder_path = os.path.split(script_path)
            config = str(os.path.join(
                folder_path[0], 'app.env'))
            return dict(dotenv_values(config))
        except Exception as e:
            print("Error at reading the env file\n", e)
            return None

    def get_download_queries(self):
        try:
            script_path = os.path.abspath(__file__)
            folder_path = os.path.split(script_path)
            return str(os.path.join(
                folder_path[0],  "sql", 'dashboard_downloads/'))
        except Exception as e:
            print("Error While reading file path", e)

    def get_dashboard_sql_path(self):
        script_path = os.path.abspath(__file__)
        folder_path = os.path.split(script_path)
        return str(os.path.join(
            folder_path[0], "sql", 'dashboard/'))

    def get_drilldown_dashboard_query_path(self):
        script_path = os.path.abspath(__file__)
        folder_path = os.path.split(script_path)
        return str(os.path.join(
            folder_path[0], "sql", 'dashboard_drilldown/'))

    def __load_ini(self):
        try:
            env_config = self.get_env_path()
            grafana_monitoring_env = env_config["GRAFANA_MONITORING_ENV"]
            if grafana_monitoring_env is None:
                raise("GRAFANA_MONITORING_ENV is missing")

            script_path = os.path.abspath(__file__)
            folder_path = os.path.split(script_path)
            ini_config = configparser.ConfigParser()
            ini_config.read(folder_path[0]+'/app.ini')
            self.ini_config = ini_config[grafana_monitoring_env.upper()]
            
        except Exception as e:
            print("Failed to load ini file: ", e)

    def replace_with_sciencelogic_dynamic_ids(self, sql):
        """
            Replace *_DID tables and *_PID ids with their values for 
            the environment set in environment variable GRAFANA_MONITORING_ENV
            dynamic app data table id = did
            presentation id = pid
        """
        try:
            for key in self.ini_config:
                sql = sql.replace(
                    str(key.upper()).strip(),
                    str(self.ini_config[key]).strip()
                )
            return sql
        except Exception as e:
            print(
                "[replace_with_sciencelogic_dynamic_ids] Error while adding DID and PIP\n", e)
            return ""
