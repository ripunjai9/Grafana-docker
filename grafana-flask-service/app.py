from flask_cors import CORS, cross_origin
import codecs
import os
from flask import Flask, send_file, request
from service import Service
import pytz
from datetime import datetime
from reports.report_services import ReportServices
from reports.report_utils import ReportUtility

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
script_path = os.path.abspath(__file__)
folder_path = os.path.split(script_path)
file_path = str(os.path.join(folder_path[0], 'saved_xls/'))
reports = ReportServices()
utils = ReportUtility()


def get_static_ist_time():
    date_time_str = str(datetime.now(pytz.timezone('Asia/Kolkata')))
    return date_time_str[:10]


@app.route("/download", methods=['GET'])
@cross_origin(supports_credentials=True)
def download_xls():
    ip_address = request.remote_addr
    session = request.cookies.get('grafana_session', default="", type=str)
    user_login_id = str(request.headers.get("Id"))
    user_login_email = str(request.headers.get("Login"))

    service = Service()
    is_valid_session = False
    if session is not None:
        is_valid_session = service.is_session_valid(
            session, ip_address, user_login_id, user_login_email, True)
    if not is_valid_session:
        return {"message": "invalid request", "status": "error"}, 401

    try:
        types = request.headers.get('Type')
        infrastructure = request.headers.get('Infrastructure')
        video_endpoint = request.headers.get('VideoEndpoint')
        audio_endpoint = request.headers.get('AudioEndpoint')
        organization_names = str(request.headers.get('Organizations'))\
            .replace("{", "").replace("}", "")\
            .split(",")
        is_admin = (
            user_login_email == "admin"
            and user_login_id == str("1"))
        if not is_admin:
            organization_names = service.get_valid_user_organizations(
                user_login_email, organization_names)

        if organization_names is None or len(organization_names) == 0:
            return {
                "message": "Invalid Organization / AD authentication failure / Email not mapped with organization",
                "status": "error"
            }, 400
        file_name = service.get_query_data(
            types, organization_names, infrastructure,
            video_endpoint, audio_endpoint)
        attachment_filename = "poly" + "_" + get_static_ist_time() + ".xlsx"
        return send_file(
            str(file_path) + file_name,
            as_attachment=True,
            attachment_filename=attachment_filename)
    except Exception as e:
        return {"message": str(e), "status": "error"}, 400


@app.route("/data", methods=['POST'])
@cross_origin(supports_credentials=True)
def get_dashboard_data():
    ip_address = request.remote_addr
    session = request.cookies.get("grafana_session", default="", type=str)
    args = request.args
    user_login_id = str(args.get("Id"))
    user_login_email = str(args.get("Login"))

    service = Service()
    is_valid_session = service.is_session_valid(
        session, ip_address, user_login_id, user_login_email, False)
    if not is_valid_session:
        return {"message": "invalid request", "status": "error"}, 401

    try:
        infrastructure = args.get('Infrastructure')
        video_endpoint = args.get('VideoEndpoint')
        audio_endpoint = args.get('AudioEndpoint')
        from_date = args.get('from')
        to_date = args.get(('to'))
        user_email = str(args.get("Login"))

        content = request.json
        organization_names = str(content.get('Organizations'))\
            .replace("{", "").replace("}", "")\
            .split(",")
        organization_device = str(content.get('device'))\
            .replace("{", "").replace("}", "")\
            .split(",")
        data_type = args.get("DataType")

        is_admin = (
            user_login_email == "admin"
            and user_login_id == str("1"))

        if not is_admin:
            organization_names = service.get_valid_user_organizations(
                user_email, organization_names)
        if organization_names is None or len(organization_names) == 0:
            return {
                "message": "Invalid Organization / AD authentication failure / Email not mapped with organization",
                "status": "error"
            }, 400

        result_dictionnary = service.get_dashboard_data(
            data_type, organization_names, infrastructure, video_endpoint,
            audio_endpoint, from_date, to_date, organization_device)
        return result_dictionnary, 200
    except Exception as e:
        return {"message": str(e), "status": "error"}, 400


@app.route("/org", methods=['GET'])
@cross_origin(supports_credentials=True)
def get_org():
    ip_address = request.remote_addr
    session = request.cookies.get("grafana_session", default="", type=str)
    args = request.args
    user_login_id = str(args.get("Id"))
    data_type = str(args.get("Type"))
    user_login_email = str(args.get("Login"))

    service = Service()
    is_valid_session = service.is_session_valid(
        session, ip_address, user_login_id, user_login_email, False)
    if not is_valid_session:
        return {"message": "invalid request", "status": "error"}, 401
    try:
        organization_name = []

        is_admin = user_login_email == "admin" and user_login_id == str("1")
        if not is_admin:
            organization_name, user_type = service.get_user_organizations(
                user_login_email)
            is_admin = str(organization_name).casefold() == 'admin'\
                or 'admin' in organization_name  \
                or str(user_type).casefold() == 'polyadmin'
        print(organization_name, is_admin)
        if organization_name is None or len(organization_name) == 0 and not is_admin:
            return {"message": "Invalid Organisation", "status": "error"}, 400
        result_dictionnary = service.get_organizations_data(
            is_admin, organization_name, data_type)
        print(result_dictionnary)
        return result_dictionnary, 200
    except Exception as e:
        return {"message": str(e), "status": "error"}, 400


@app.route("/test", methods=['GET'])
@cross_origin(supports_credentials=True)
def test():
    return {"message": "Test Connection", "status": "success"}, 200


@app.route("/report", methods=['POST'])
@cross_origin(supports_credentials=True)
def report_xls():
    ip_address = request.remote_addr
    session = request.cookies.get('grafana_session', default="", type=str)
    user_login_id = str(request.headers.get("Id"))
    user_login_email = str(request.headers.get("Login"))

    service = Service()
    is_valid_session = service.is_session_valid(
        session, ip_address, user_login_id, user_login_email, True)
    if not is_valid_session:
        return {"message": "invalid request", "status": "error"}, 401

    try:
        types = request.headers.get('Type')
        content = request.json
        organization_names = str(content.get('Organizations'))\
            .replace("{", "").replace("}", "")\
            .split(",")
        devices_by_organization = str(content.get('DevicesByOrganization'))\
            .replace("{", "").replace("}", "")\
            .split(",")

        is_admin = (
            user_login_email == "admin"
            and user_login_id == str("1"))

        if not is_admin:
            organization_names = service.get_valid_user_organizations(
                user_login_email, organization_names)
        if organization_names is None or len(organization_names) == 0:
            return {
                "message": "Invalid organization/ AD authentication failure/ Email not mapped with organization",
                "status": "error"
            }, 400
        file_name = reports.generate_reports(
            types, request, organization_names, devices_by_organization)

        if "error" in file_name:
            return {"message": "invalid request", "status": "error"}, 400
        sendingFileName = "poly_" + get_static_ist_time() + ".xlsx"
        return send_file(
            str(utils.get_report_path()) + file_name, as_attachment=True,
            attachment_filename=sendingFileName)

    except Exception as e:
        return {"message": str(e), "status": "error"}, 400


@app.route("/alldata", methods=['POST'])
@cross_origin(supports_credentials=True)
def get_alldata():
    ip_address = request.remote_addr
    session = request.cookies.get("grafana_session", default="", type=str)
    args = request.args
    content = request.json
    user_login_id = str(args.get("Id"))
    user_login_email = str(args.get("Login"))

    service = Service()
    is_valid_session = service.is_session_valid(
        session, ip_address, user_login_id, user_login_email, False)
    if not is_valid_session:
        return {"message": "invalid request", "status": "error"}, 401

    try:
        infrastructure = args.get('Infrastructure')
        video_endpoint = args.get('VideoEndpoint')
        audio_endpoint = args.get('AudioEndpoint')
        organization_name = str(content.get('Organizations'))\
            .replace("{", "").replace("}", "")\
            .split(",")
        data_type = args.get("DataType")

        is_admin = (
            user_login_email == "admin"
            and user_login_id == str("1")
        )

        if not is_admin:
            organization_name = service.get_valid_user_organizations(
                args.get("Login"), organization_name)

        if organization_name is None or len(organization_name) == 0:
            return {
                "message": "Invalid Organization / AD authentication failure/ Email not mapped with organization",
                "status": "error"
            }, 400

        result_dict = service.get_drilldown_data(
            data_type, organization_name, infrastructure,
            video_endpoint, audio_endpoint)
        return result_dict, 200
    except Exception as e:
        return {"message": str(e), "status": "error"}, 400


@app.route("/multi_tenancy", methods=['GET'])
@cross_origin(supports_credentials=True)
def get_multi_tenancy_data():
    ip_address = request.remote_addr
    session = request.cookies.get("grafana_session", default="", type=str)
    args = request.args
    user_login_id = str(args.get("Id"))
    data_type = str(args.get("Type"))
    user_login_email = str(args.get("Login"))

    service = Service()
    is_valid_session = service.is_session_valid(
        session, ip_address, user_login_id, user_login_email, False)
    if not is_valid_session:
        return {"message": "invalid request", "status": "error"}, 401
    try:
        is_admin = user_login_email == "admin" and user_login_id == str("1")

        if not is_admin:
            organization_name = service.validate_poly_user(
                args.get("Login"))
            is_admin = str(organization_name).casefold() == 'polyadmin'
        if not is_admin:
            return {"message": "invalid request", "status": "error"}, 401

        result_dictionary = service.get_multi_tenancy_data(data_type)
        return result_dictionary, 200
    except Exception as e:
        return {"message": str(e), "status": "error"}, 400


@app.route("/add_user_organization", methods=['POST'])
@cross_origin(supports_credentials=True)
def add_organization_to_user():
    ip_address = request.remote_addr
    session = request.cookies.get("grafana_session", default="", type=str)

    user_login_id = str(request.headers.get("Id"))
    user_login_email = str(request.headers.get("Login"))

    service = Service()
    is_valid_session = service.is_session_valid(
        session, ip_address, user_login_id, user_login_email, False)
    if not is_valid_session:
        return {"message": "invalid request", "status": "error"}, 401

    content = request.json
    organization = str(content.get('Organizations'))\
        .replace("{", "").replace("}", "")\
        .split(",")
    user_email = str(content.get('user')).replace("{", "").replace("}", "")

    if (
        organization is None
        or len(organization) == 0
        or user_email is None
        or len(user_email) == 0
    ):
        return {"message": "User organization and email is mandatory", "status": "error"}, 400

    try:
        is_admin = (user_login_email == "admin") and (
            user_login_id == str("1"))
        if not is_admin:
            user_role = service.validate_poly_user(user_login_email)
            is_admin = str(user_role).casefold() == 'polyadmin'
            # is_admin = True

        if not is_admin:
            return {"message": "invalid request", "status": "error"}, 401

        message, status = service.add_organization_to_user(
            organization, user_email)
        if status == "success":
            return {"message": message, "status": "success"}, 200
        else:
            return {"message": message, "status": "error"}, 400
    except Exception as e:
        return {"message": str(e), "status": "error"}, 400


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000, debug=True)
