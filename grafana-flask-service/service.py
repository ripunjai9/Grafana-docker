from logging import exception
from poly_active_directory import PolyActiveDirectory
from grafana_db import GrafanaDb
import re
from xls_writer import XlsWriter
import hashlib
from dashboard_downloads_sql_helpers import DashboardDownloadsSqlHelpers
from dashboard import Dashboard
from dashboard_drilldown import DashboardDrilldown

from graphql.graphql_data import GraphqlData
from graphql.graphql_drilldown_query import GraphqlDrilldownData
from graphql.graphql_download_query import GraphqlDownloadData
from sciencelogic_db import ScienceLogicDb

from graphql.graphql_util import GraphQLUtil


def get_secret_key(file_data):
    final_secret_key = ""
    if "secret_key" in file_data:
        res_1 = set(re.findall("secret_key = .*", file_data))
        res_2 = re.findall(";secret_key = .*", file_data)
        for secret_key in res_1:
            if secret_key not in str(res_2):
                final_secret_key = secret_key
    return None if len(final_secret_key) == 0 or final_secret_key is None else str(
        final_secret_key.split("=")[1]).strip()


def get_security_token():
    f = open("/etc/grafana/grafana.ini", "r", encoding='utf-8')
    # f = open("./grafana.ini", "r", encoding='utf-8')
    _token = get_secret_key(str(f.read()))
    if _token is None:
        f = open("/usr/share/grafana/conf/defaults.ini", "r", encoding='utf-8')
        # f = open("./defaults.ini", "r", encoding='utf-8')
        _token = get_secret_key(str(f.read()))
    return _token


_token = get_security_token()
static_query = DashboardDownloadsSqlHelpers()
dashboard = Dashboard()
dashboard_drilldown = DashboardDrilldown()
graphql_util = GraphQLUtil()
graphql_data = GraphqlData()
graphql_drilldown_data = GraphqlDrilldownData()
graphql_download_data = GraphqlDownloadData()


class Service:
    def __init__(self):
        self.sciencelogic_db = ScienceLogicDb()
        self.grafana_db = GrafanaDb()
        self.poly_active_directory = PolyActiveDirectory()

    def get_query_data(
        self, type, organization_names,
            infrastructure, video_endpoint, audio_endpoint
    ):
        try:
            if not isinstance(organization_names, list):
                organization_names = [organization_names]
            if "graphql" in type:
                return graphql_download_data.get_query(
                    type, organization_names, infrastructure,
                    video_endpoint, audio_endpoint)
            else:
                query_dict = static_query.get_query(
                    type, organization_names, infrastructure,
                    video_endpoint, audio_endpoint)
                xls_dict = {}
                for key, data_query in query_dict.items():
                    data_list = self.sciencelogic_db.execute(
                        data_query.get("query"), data_query.get("params"), True)
                    xls_dict[key] = data_list
                xls = XlsWriter()
                file_name = xls.write_data_xls(xls_dict)
                return file_name
        except Exception as e:
            return ""

    def is_session_valid(
        self, session_id, ip_address, user_login_id,
        user_login_detail, is_ip_checked
    ):
        try:
            if session_id is None and len(session_id) == 0:
                return False
            secret_key = self.get_authentication_token(
                session_id.encode(), _token.encode())

            return self.grafana_db.is_session_valid(
                str(secret_key).strip(), str(ip_address),
                str(user_login_id), str(user_login_detail),
                is_ip_checked)
        except Exception as e:
            print("Error: While validating the session id\n", e)
            return False

    def get_authentication_token(self, _token, _secret_key):
        _concatenated = _token + _secret_key
        return hashlib.sha256(_concatenated).hexdigest()

    def validate_user_organization(self, user_email, organization):
        return self.poly_active_directory.get_valid_user_organization(
            user_email, organization)

    def get_dashboard_data(
            self, data_type, organization_names, infrastructure, video_endpoint,
            audio_endpoint, from_date, to_date, devices):
        try:
            if not isinstance(organization_names, list):
                organization_names = [organization_names]
            if not isinstance(devices, list):
                devices = [devices]

            if "graphql" in data_type:
                return graphql_data.get_query(
                    data_type, organization_names, str(infrastructure),
                    str(video_endpoint), str(audio_endpoint))
            else:
                return dashboard.get_query(
                    data_type, organization_names,
                    str(infrastructure), str(video_endpoint),
                    str(audio_endpoint), str(from_date),
                    str(to_date), devices)
        except Exception as e:
            print(e)
            return {}

    def get_drilldown_data(
        self, data_type, organization_names, infrastructure,
        video_endpoint, audio_endpoint
    ):
        try:
            if not isinstance(organization_names, list):
                organization_names = [organization_names]

            if "graphql" in data_type:
                return graphql_drilldown_data.get_query(
                    data_type, organization_names, str(infrastructure),
                    str(video_endpoint), str(audio_endpoint))
            else:
                return dashboard_drilldown.get_query(
                    data_type, organization_names, str(infrastructure),
                    str(video_endpoint), str(audio_endpoint))
        except Exception as e:
            return {}

    def get_organizations_data(self, is_admin, organization_names, request_type):
        try:
            if request_type is not None and request_type in 'graphql':
                return self.gql_get_organizations_data(is_admin, organization_names)
            # organization_names = str(organization_names).split(",")
            # if not isinstance(organization_names, list):
            #     organization_names = [organization_names]

            if is_admin:
                sql = "SELECT company FROM master_biz.organizations"
                organization_names = []
            else:
                sql = "SELECT company FROM master_biz.organizations WHERE company IN %s"
                organization_names = (organization_names,)

            data_list = self.sciencelogic_db.execute(
                sql, organization_names)
            final_list = []
            for dt in data_list:
                final_list.append(dt[0])
            final_dict = {"result": final_list}
            return final_dict
        except Exception as e:
            return "", {}

    def gql_get_organizations_data(self, is_admin, organization_names):
        try:
            organization_names = str(organization_names).split(",")
            if not isinstance(organization_names, list):
                organization_names = [organization_names]

            # for org in organization_names:
            #     if "all" != str(org).lower().strip() and is_admin:
            #         is_admin = False

            if is_admin:
                gql = """query OrganizationDetails($TotalCount: Int){
                      organizations(first:$TotalCount) {
                        pageInfo{
                          matchCount
                        }
                        edges {
                          node {
                            company
                          }
                        }
                      }
                    }
                    """
                variable = {
                    "TotalCount": 1
                }
            else:
                gql = """
                query Organization($Org: [String], $TotalCount: Int) {
                  organizations(search: {company: {in: $Org}}, first:$TotalCount) {
                    pageInfo {
                      matchCount
                    }
                    edges {
                      node {
                        company
                      }
                    }
                  }
                }

                """
                variable = {
                    "Org": organization_names,
                    "TotalCount": 1
                }
            response = graphql_util.request_graphql_api(gql, variable)
            total_count = int(response.get("data").get(
                "organizations").get("pageInfo").get("matchCount"))
            variable["TotalCount"] = total_count

            response = graphql_util.request_graphql_api(gql, variable)
            final_list = []
            for company in response.get("data").get("organizations").get("edges"):
                final_list.append(company.get("node").get("company"))

            final_dict = {"result": final_list}

            return final_dict
        except Exception as e:
            return "", {}

    def get_multi_tenancy_data(self, data_type):
        if "poly_organization" == data_type:
            try:
                sql = "SELECT company FROM master_biz.organizations"
                organizations = self.sciencelogic_db.execute(sql, [])
                self.grafana_db.update_user_organisations(organizations)
                final_list = []
                for organization in organizations:
                    final_list.append(organization[0])
                final_dict = {"result": final_list}
                return final_dict
            except Exception as e:
                return {}

        elif "poly_user" == data_type:
            try:
                poly_azure_emails = self.poly_active_directory.get_users()
                self.grafana_db.update_users(poly_azure_emails)
                final_dict = {"result": poly_azure_emails}
                return final_dict
            except Exception as e:
                return {}
        elif "poly_organization_user_mapping_table" == data_type:
            try:
                poly_user_organization_dict = self.grafana_db.get_poly_user_organization_list()
                if (
                    poly_user_organization_dict is not None
                    and len(poly_user_organization_dict) > 0
                ):
                    filtered_user_organizations = []
                    for key, value in poly_user_organization_dict.items():
                        temp_dict = {
                            "user": str(key),
                            "organization": str(value)
                            .replace("[", "").replace("]", "").replace("'", "")
                        }
                        filtered_user_organizations.append(temp_dict)
                    return {"result": filtered_user_organizations}
                else:
                    return {"result": []}
            except Exception as e:
                return {}
        else:
            return {}

    def validate_poly_user(self, user_email):
        return self.poly_active_directory.validate_poly_user(user_email)

    def add_organization_to_user(self, organization, email):
        if not isinstance(organization, list):
            organization = [organization]
        return self.grafana_db.add_organization_to_user(organization, email)

    def get_user_organizations(self, email):
        user_type = self.poly_active_directory.validate_poly_user(email)
        print("user_type", user_type)
        if (
            str(user_type).casefold() == 'admin'
            or str(user_type).casefold() == 'polyadmin'
        ):
            return ["admin"], user_type
        elif str(user_type).casefold() == 'user':
            user_organizations = self.grafana_db.get_user_organization(email)
            if user_organizations is None or len(user_organizations) == 0:
                return [], user_type
            return user_organizations, user_type
        else:
            return [], None

    def get_valid_user_organizations(
        self, email, organizations
    ):
        user_type = self.poly_active_directory.validate_poly_user(email)
        if (
            str(user_type).casefold() == 'admin'
            or str(user_type).casefold() == 'polyadmin'
        ):
            return organizations

        elif str(user_type).casefold() == 'user':
            user_organizations = self.grafana_db.get_user_organization(email)
            if user_organizations is None or len(user_organizations) == 0:
                return []
            else:
                for organization in organizations:
                    if organization not in user_organizations:
                        return None
            return organizations
        else:
            return []
