from sciencelogic_db import ScienceLogicDb
from helpers import Helpers
from reports.report_utils import ReportUtility

helper = Helpers()
utils = ReportUtility()


class Dashboard:
    def __init__(self):
        self.sciencelogic_db = ScienceLogicDb()

    def get_query(self, type, organization_name, infrastructure, video_endpoint, audio_endpoint, from_date, to_date, org_device):

        if type in "all_devices_count":
            return self.device_count(organization_name)
        elif type in "all_devices_alarm_count":
            return self.devices_alarm_count(organization_name)
        elif type in "all_devices_down_count":
            return self.devices_down_count(organization_name)
        elif type in "all_devices_alarm_details":
            return self.device_alarm_details(organization_name)

        elif type in "infrastructure_devices_count":
            return self.infrastructure_device_count(organization_name, infrastructure)
        elif type in "infrastructure_devices_alarm_count":
            return self.infrastructure_device_alarm_count(organization_name, infrastructure)
        elif type in "infrastructure_devices_down_count":
            return self.infrastructure_device_down_count(organization_name, infrastructure)
        elif type in "infrastructure_devices_alarm_details":
            return self.infrastructure_alarm_details(organization_name, infrastructure)

        elif type in "video_endpoints_count":
            return self.video_endpoints_device_count(organization_name, video_endpoint)
        elif type in "video_endpoints_alarm_count":
            return self.video_endpoints_alarm_count(organization_name, video_endpoint)
        elif type in "video_endpoints_down_count":
            return self.video_endpoints_down_count(organization_name, video_endpoint)
        elif type in "video_endpoints_alarm_details":
            return self.video_endpoints_alarm_details(organization_name, video_endpoint)

        elif type in "audio_endpoints_count":
            return self.audio_endpoints_device_count(organization_name, audio_endpoint)
        elif type in "audio_endpoints_alarm_count":
            return self.audio_endpoints_alarm_count(organization_name, audio_endpoint)
        elif type in "audio_endpoints_down_count":
            return self.audio_endpoints_down_count(organization_name, audio_endpoint)
        elif type in "audio_endpoints_alarm_details":
            return self.audio_endpoints_alarm_details(organization_name, audio_endpoint)

        elif type in "top_10_problematic_devices_count":
            return self.eventDevice_device_count(organization_name)
        elif type in "top_10_events_count":
            return self.problematic_devices(organization_name)

        elif type in "top_5_memory_usage":
            return self.top_memory_usage(organization_name, infrastructure)
        elif type in "top_5_cpu_usage":
            return self.top_cpu_usage(organization_name, infrastructure)

        elif type in "all_devices_availability_excluding_infrastructure":
            return self.all_devices_excluding_infrastructure(organization_name, infrastructure)
        elif type in "all_infrastructure_devices_availability":
            return self.all_devices_including_infrastructure(organization_name, infrastructure)

        elif type in "device_count_by_vendor":
            return self.vendor_device_count(organization_name)
        elif type in "device_count_by_category":
            return self.category_device_count_dashboard(organization_name)
        elif type in "device_count_by_location_category":
            return self.device_count_by_location_category(organization_name)
        elif type in "certificate_expiration":
            return self.certificate_expiration(organization_name, infrastructure)

        elif type in "device_port_usage_percentage":
            return self.device_port_usage_percentage(organization_name, infrastructure)
        elif type in "device_license_usage_percentage":
            return self.device_license_usage_percentage(organization_name, infrastructure)

        elif type in "top_endpoints_packet_loss":
            return self.top_end_point_packet_loss(organization_name)

        elif type in "scheduled_maintenance":
            return self.scheduled_maintenance_table(organization_name)

        elif type in "port_graph_usage_devices":
            return self.port_usage_devices(organization_name, infrastructure)
        elif type in "video_port_usage_infrastructure":
            return self.video_port_usage_infrastructure(org_device, from_date, to_date)
        elif type in "license_usage_infrastructure_1":
            return self.license_usage_infrastructure_1(org_device, from_date, to_date)
        elif type in "license_usage_infrastructure_2":
            return self.license_usage_infrastructure_2(org_device, from_date, to_date)
        elif type in "license_usage_infrastructure_3":
            return self.license_usage_infrastructure_3(org_device, from_date, to_date)
        elif type in "license_usage_devices":
            return self.license_usage_devices(organization_name, infrastructure)

        elif type in "packet_loss_drilldown_devices":
            return self.packet_loss_drill_down_devices(organization_name)

        elif type in "packet_loss_content_1":
            return self.packet_loss_content_1(org_device, from_date, to_date)
        elif type in "packet_loss_content_2":
            return self.packet_loss_content_2(org_device, from_date, to_date)
        elif type in "video_packet_lost_1":
            return self.video_packet_lost_1(org_device, from_date, to_date)
        elif type in "video_packet_lost_2":
            return self.video_packet_lost_2(org_device, from_date, to_date)
        elif type in "audio_packet_lost_1":
            return self.audio_packet_lost_1(org_device, from_date, to_date)
        elif type in "audio_packet_lost_2":
            return self.audio_packet_lost_2(org_device, from_date, to_date)

        elif type in "download_report_devices":
            return self.download_reports_devices(organization_name)
        else:
            return {}

    def device_count(self, organizations):
        try:
            sql = self.read_sql_file("all_devices/device_count")
            params = (organizations,)
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": data_list[0][0]}
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def devices_alarm_count(self, organizations):
        try:
            sql = self.read_sql_file("all_devices/alarm_count")
            params = (organizations,)
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": data_list[0][0]}
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def devices_down_count(self, organizations):
        try:
            sql = self.read_sql_file("all_devices/down_count")
            params = (organizations,)
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": data_list[0][0]}
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def device_alarm_details(self, organizations):
        try:
            sql = self.read_sql_file("all_devices/alarm_details")
            params = (organizations,)
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {}
            for data in data_list:
                final_dict[data[1]] = data[0]
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def infrastructure_device_count(self, organizations, infrastructure):
        try:
            sql = self.read_sql_file("infrastructure/device_count")
            params = (organizations, str(infrastructure))
            data_list = self.sciencelogic_db.execute(sql, params)
            if data_list is not None and len(data_list) > 0:
                return {"result": data_list[0][0]}
            return {"result": "error"}
        except Exception as e:
            print(e)
            return {}

    def infrastructure_device_alarm_count(self, organizations, infrastructure):
        try:
            sql = self.read_sql_file("infrastructure/alarm_count")
            params = (organizations, str(infrastructure))
            data_list = self.sciencelogic_db.execute(sql, params)
            if data_list is not None and len(data_list) > 0:
                return {"result": data_list[0][0]}
            return {"result": "error"}
        except Exception as e:
            print(e)
            return {}

    def infrastructure_device_down_count(self, organizations, infrastructure):
        try:
            sql = self.read_sql_file("infrastructure/down_count")
            params = (organizations, str(infrastructure))
            data_list = self.sciencelogic_db.execute(sql, params)
            if data_list is not None and len(data_list) > 0:
                return {"result": data_list[0][0]}
            return {"result": "error"}
        except Exception as e:
            print(e)
            return {}

    def infrastructure_alarm_details(self, organizations, infrastructure):
        try:
            sql = self.read_sql_file("infrastructure/alarm_details")
            params = (organizations, infrastructure)
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {}
            for data in data_list:
                final_dict[data[1]] = data[0]
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def video_endpoints_device_count(self, organizations, video_endpoint):
        try:
            sql = self.read_sql_file("video_endpoints/device_count")
            params = (organizations, str(video_endpoint))
            data_list = self.sciencelogic_db.execute(sql, params)
            if data_list is not None and len(data_list) > 0:
                return {"result": data_list[0][0]}
            return {"result": "error"}
        except Exception as e:
            print(e)
            return {}

    def video_endpoints_alarm_count(self, organization_name, video_endpoint):
        try:
            sql = self.read_sql_file("video_endpoints/alarm_count")
            params = (organization_name, str(video_endpoint))
            data_list = self.sciencelogic_db.execute(sql, params)
            if data_list is not None and len(data_list) > 0:
                return {"result": data_list[0][0]}
            return {"result": "error"}
        except Exception as e:
            print(e)
            return {}

    def video_endpoints_down_count(self, organization_name, video_endpoint):
        try:
            sql = self.read_sql_file("video_endpoints/down_count")
            params = (organization_name, str(video_endpoint))
            data_list = self.sciencelogic_db.execute(sql, params)
            if data_list is not None and len(data_list) > 0:
                return {"result": data_list[0][0]}
            return {"result": "error"}
        except Exception as e:
            print(e)
            return {}

    def video_endpoints_alarm_details(self, organizations, video_endpoint):
        try:
            sql = self.read_sql_file("video_endpoints/alarm_details")
            params = (organizations, video_endpoint)
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {}
            for data in data_list:
                final_dict[data[1]] = data[0]
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def audio_endpoints_device_count(self, organization_name, audio_endpoint):
        try:
            sql = self.read_sql_file("audio_endpoints/device_count")
            params = (organization_name, str(audio_endpoint))
            data_list = self.sciencelogic_db.execute(sql, params)
            if data_list is not None and len(data_list) > 0:
                return {"result": data_list[0][0]}
            return {"result": "error"}
        except Exception as e:
            print(e)
            return {}

    def audio_endpoints_alarm_count(self, organization_name, audio_endpoint):
        try:
            sql = self.read_sql_file("audio_endpoints/alarm_count")
            params = (organization_name, str(audio_endpoint))
            data_list = self.sciencelogic_db.execute(sql, params)
            if data_list is not None and len(data_list) > 0:
                return {"result": data_list[0][0]}
            return {"result": "error"}
        except Exception as e:
            print(e)
            return {}

    def audio_endpoints_down_count(self, organization_name, audio_endpoint):
        try:
            sql = self.read_sql_file("audio_endpoints/down_count")
            params = (organization_name, str(audio_endpoint))
            data_list = self.sciencelogic_db.execute(sql, params)
            if data_list is not None and len(data_list) > 0:
                return {"result": data_list[0][0]}
            return {"result": "error"}
        except Exception as e:
            print(e)
            return {}

    def audio_endpoints_alarm_details(self, organization_name, audio_endpoint):
        try:
            sql = self.read_sql_file("audio_endpoints/alarm_details")
            params = (organization_name, audio_endpoint)
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {}
            for data in data_list:
                final_dict[data[1]] = data[0]
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def eventDevice_device_count(self, organization_name):
        try:
            sql = self.read_sql_file("top/10/event_count")
            params = (organization_name,)
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": []}
            count = 0
            for data in data_list:
                temp_dict = {
                    "time": data[0],
                    "message": data[1],
                    "count": data[2]
                }
                count += 1
                final_dict.get("result").append(temp_dict)
            if count < 10:
                star = 1
                while True:
                    if count == 10:
                        break
                    star_string = ""
                    for i in range(0, star):
                        star_string += "."
                    temp_dict = {
                        "time": "-1",
                        "message": star_string,
                        "count": "0"
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
            sql = self.read_sql_file("top/10/problematic_devices")
            params = (organization_name,)
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": []}
            count = 0
            for data in data_list:
                temp_dict = {
                    "time": data[0],
                    "deviceName": data[1],
                    "count": data[2]
                }
                count += 1
                final_dict.get("result").append(temp_dict)
            if count < 10:
                while True:
                    if count == 10:
                        break
                    temp_dict = {
                        "time": "-1",
                        "deviceName": ".",
                        "count": "0"
                    }
                    count += 1
                    final_dict.get("result").append(temp_dict)
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def top_memory_usage(self, organization_name, infrastructure):
        try:
            sql = self.read_sql_file("top/5/memory_usage")
            params = (organization_name, infrastructure)
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": []}
            count = 0
            for data in data_list:
                temp_dict = {
                    "time": data[0],
                    "device": data[1],
                    "peak_memory": data[2]
                }
                count += 1
                final_dict.get("result").append(temp_dict)
            if count < 5:
                while True:
                    if count == 5:
                        break
                    temp_dict = {
                        "time": "-1",
                        "device": ".",
                        "peak_memory": "0"
                    }
                    count += 1
                    final_dict.get("result").append(temp_dict)
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def top_cpu_usage(self, organization_name, infrastructure):
        try:
            sql = self.read_sql_file("top/5/cpu_usage")
            params = (organization_name, infrastructure)
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": []}
            count = 0
            for data in data_list:
                temp_dict = {
                    "time": data[0],
                    "device": data[1],
                    "peak_memory": data[2]
                }
                count += 1
                final_dict.get("result").append(temp_dict)
            if count < 5:
                while True:
                    if count == 5:
                        break
                    temp_dict = {
                        "time": "-1",
                        "device": ".",
                        "peak_memory": "0"
                    }
                    count += 1
                    final_dict.get("result").append(temp_dict)
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def all_devices_excluding_infrastructure(self, organization_name, infrastructure):
        try:
            sql = self.read_sql_file(
                "availability/all_devices_excluding_infrastructure")
            params = (organization_name, infrastructure)
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": []}
            count = 0
            for data in data_list:
                temp_dict = {
                    "time": data[0],
                    "device": data[2],
                    "average": data[1]
                }
                count += 1
                final_dict.get("result").append(temp_dict)
            if count < 10:
                while True:
                    if count == 10:
                        break
                    temp_dict = {
                        "time": "-1",
                        "device": ".",
                        "average": "0"
                    }
                    count += 1
                    final_dict.get("result").append(temp_dict)
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def all_devices_including_infrastructure(self, organization_name, infrastructure):
        try:
            sql = self.read_sql_file("availability/infrastructure_devices")
            params = (organization_name, infrastructure)
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": []}
            count = 0
            for data in data_list:
                temp_dict = {
                    "time": data[0],
                    "device": data[2],
                    "average": data[1]
                }
                count += 1
                final_dict.get("result").append(temp_dict)
            if count < 10:
                while True:
                    if count == 10:
                        break
                    temp_dict = {
                        "time": "-1",
                        "device": ".",
                        "average": "0"
                    }
                    count += 1
                    final_dict.get("result").append(temp_dict)
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def vendor_device_count(self, organization_name):
        try:
            sql = self.read_sql_file("device_count_by_vendor")
            params = (organization_name,)
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": []}
            count = 0
            for data in data_list:
                temp_dict = {
                    "time": data[0],
                    "value": data[1],
                    "metric": data[2]
                }
                count += 1
                final_dict.get("result").append(temp_dict)
            if count < 10:
                star = 1
                while True:
                    if count == 10:
                        break
                    star_string = ""
                    for i in range(0, star):
                        star_string += "."
                    temp_dict = {
                        "time": "-1",
                        "value": "0",
                        "metric": star_string
                    }
                    count += 1
                    star += 1
                    final_dict.get("result").append(temp_dict)
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def category_device_count_dashboard(self, organization_name):
        try:
            sql = self.read_sql_file("device_count_by_category")
            params = (organization_name,)
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": []}
            count = 0
            for data in data_list:
                temp_dict = {
                    "time": data[0],
                    "value": data[1],
                    "metric": data[2]
                }
                count += 1
                final_dict.get("result").append(temp_dict)
            if count < 10:
                star = 1
                while True:
                    if count == 10:
                        break
                    star_string = ""
                    for i in range(0, star):
                        star_string += "."
                    temp_dict = {
                        "time": "-1",
                        "value": "0",
                        "metric": star_string
                    }
                    count += 1
                    star += 1
                    final_dict.get("result").append(temp_dict)
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def device_count_by_location_category(self, organization_name):
        try:
            sql = self.read_sql_file("device_count_by_location_category")
            params = (organization_name,)
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": []}
            for data in data_list:
                temp_dict = {
                    "location": data[0],
                    "category": data[1],
                    "count": data[2]
                }
                final_dict.get("result").append(temp_dict)
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def certificate_expiration(self, organization_name, infrastructure):
        try:
            sql = self.read_sql_file("certificate_expiration")
            params = (organization_name, infrastructure)
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": []}
            for data in data_list:
                temp_dict = {
                    "certificate_organization": data[0],
                    "expiration_date": data[1],
                    "days_left": data[2],
                    "cert_id": data[3],
                    "device_name": data[4],
                    "ip": data[5],
                    "device_category": data[6],
                    "device_type": data[7],
                    "organization": data[8]
                }
                final_dict.get("result").append(temp_dict)
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def device_port_usage_percentage(self, organization_name, infrastructure):
        try:
            sql = self.read_sql_file("device_port_utilization_percentage")
            params = (organization_name, infrastructure)
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": []}
            count = 0
            for data in data_list:
                temp_dict = {
                    "time": data[0],
                    "device": data[1],
                    "average": data[2]
                }
                count += 1
                final_dict.get("result").append(temp_dict)
            if count < 5:
                while True:
                    if count == 5:
                        break
                    temp_dict = {
                        "time": "-1",
                        "device": ".",
                        "average": "0"
                    }
                    count += 1
                    final_dict.get("result").append(temp_dict)
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def device_license_usage_percentage(self, organization_name, infrastructure):
        try:
            sql = self.read_sql_file("device_license_utilization_percentage")
            params = (organization_name, infrastructure)
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": []}
            count = 0
            for data in data_list:
                temp_dict = {
                    "time": data[0],
                    "device": data[1],
                    "average": data[2]
                }
                count += 1
                final_dict.get("result").append(temp_dict)
            if count < 5:
                while True:
                    if count == 5:
                        break
                    temp_dict = {
                        "time": "-1",
                        "device": ".",
                        "average": "0"
                    }
                    count += 1
                    final_dict.get("result").append(temp_dict)
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def top_end_point_packet_loss(self, organization_name):
        try:
            sql = self.read_sql_file("packet_loss/top_end_point_packet_loss")
            params = (organization_name, )
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": []}
            for data in data_list:
                temp_dict = {
                    "time": data[0],
                    "device": data[1],
                    "average": data[2]
                }
                final_dict.get("result").append(temp_dict)
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def scheduled_maintenance_table(self, organization_name):
        try:
            sql = self.read_sql_file("scheduled_maintenance")
            params = (organization_name,)
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": []}
            for data in data_list:
                temp_dict = {
                    "device_name": data[0],
                    "device_category": data[1],
                    "device_type": data[2],
                    "schedule_summary": data[3],
                    "schedule_description": data[4],
                    "schedule_start_date": data[5],
                    "schedule_end_date": data[6]
                }
                final_dict.get("result").append(temp_dict)
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def port_usage_devices(self, organization_name, infrastructure):
        try:
            sql = self.read_sql_file("port_graph_utilizations_devices")
            params = (organization_name, infrastructure)
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": []}
            for dt in data_list:
                final_dict.get("result").append(dt[0])
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def video_port_usage_infrastructure(self, organization_name, from_date, to_date):
        try:
            from_date = utils.get_datetime(from_date)
            to_date = utils.get_datetime(to_date)
            sql = self.read_sql_file("video_port_usage_graph_infrastructure")
            params = (organization_name, from_date, to_date)
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": []}
            for data in data_list:
                temp_dict = {
                    "time": data[0],
                    "total_avail": data[1],
                    "type": data[2]
                }
                final_dict.get("result").append(temp_dict)
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def license_usage_infrastructure_1(self, organization_name, from_date, to_date):
        try:
            from_date = utils.get_datetime(from_date)
            to_date = utils.get_datetime(to_date)
            sql = self.read_sql_file("license_usage/graph_infrastructure_1")
            params = (organization_name, from_date, to_date)
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": []}
            for data in data_list:
                temp_dict = {
                    "time": data[0],
                    "total_avail": data[1],
                    "type": data[2]
                }
                final_dict.get("result").append(temp_dict)
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def license_usage_infrastructure_2(self, organization_name, from_date, to_date):
        try:
            from_date = utils.get_datetime(from_date)
            to_date = utils.get_datetime(to_date)
            sql = self.read_sql_file("license_usage/graph_infrastructure_2")
            params = (organization_name, from_date, to_date)
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": []}
            for data in data_list:
                temp_dict = {
                    "time": data[0],
                    "total_avail": data[1],
                    "type": data[2]
                }
                final_dict.get("result").append(temp_dict)
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def license_usage_infrastructure_3(self, organization_name, from_date, to_date):
        try:
            from_date = utils.get_datetime(from_date)
            to_date = utils.get_datetime(to_date)
            sql = self.read_sql_file("license_usage/graph_infrastructure_3")
            params = (organization_name, from_date, to_date)
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": []}
            for data in data_list:
                temp_dict = {
                    "time": data[0],
                    "total_avail": data[1],
                    "type": data[2]
                }
                final_dict.get("result").append(temp_dict)
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def license_usage_devices(self, organization_name, infrastructure):
        try:
            sql = self.read_sql_file("license_graph_utilizations_devices")
            params = (organization_name, infrastructure)
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": []}
            for dt in data_list:
                final_dict.get("result").append(dt[0])
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def packet_loss_drill_down_devices(self, organization_name):
        try:
            sql = self.read_sql_file("packet_loss/drill_down_devices")
            params = (organization_name, )
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": []}
            for dt in data_list:
                final_dict.get("result").append(dt[0])
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def packet_loss_content_1(self, organization_name, from_date, to_date):
        try:
            from_date = utils.get_datetime(from_date)
            to_date = utils.get_datetime(to_date)
            sql = self.read_sql_file("packet_loss/content_1")
            params = (organization_name, from_date, to_date)
            data_list = self.sciencelogic_db.execute(sql, params)

            final_dict = {"result": []}
            for data in data_list:
                temp_dict = {
                    "time": data[0],
                    "total_avail": data[1],
                    "type": data[2]
                }
                final_dict.get("result").append(temp_dict)
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def packet_loss_content_2(self, organization_name, from_date, to_date):
        try:
            from_date = utils.get_datetime(from_date)
            to_date = utils.get_datetime(to_date)
            sql = self.read_sql_file("packet_loss/content_2")
            params = (organization_name, from_date, to_date)
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": []}
            for data in data_list:
                temp_dict = {
                    "time": data[0],
                    "total_avail": data[1],
                    "type": data[2]
                }
                final_dict.get("result").append(temp_dict)
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def video_packet_lost_1(self, organization_name, from_date, to_date):
        try:
            from_date = utils.get_datetime(from_date)
            to_date = utils.get_datetime(to_date)
            sql = self.read_sql_file("packet_loss/video_1")
            params = (organization_name, from_date, to_date)
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": []}
            for data in data_list:
                temp_dict = {
                    "time": data[0],
                    "total_avail": data[1],
                    "type": data[2]
                }
                final_dict.get("result").append(temp_dict)
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def video_packet_lost_2(self, organization_name, from_date, to_date):
        try:
            from_date = utils.get_datetime(from_date)
            to_date = utils.get_datetime(to_date)
            sql = self.read_sql_file("packet_loss/video_2")
            params = (organization_name, from_date, to_date)
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": []}
            for data in data_list:
                temp_dict = {
                    "time": data[0],
                    "total_avail": data[1],
                    "type": data[2]
                }
                final_dict.get("result").append(temp_dict)
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def audio_packet_lost_1(self, organization_name, from_date, to_date):
        try:
            from_date = utils.get_datetime(from_date)
            to_date = utils.get_datetime(to_date)
            sql = self.read_sql_file("packet_loss/audio_1")
            params = (organization_name, from_date, to_date)
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": []}
            for data in data_list:
                temp_dict = {
                    "time": data[0],
                    "total_avail": data[1],
                    "type": data[2]
                }
                final_dict.get("result").append(temp_dict)
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def audio_packet_lost_2(self, organization_name, from_date, to_date):
        try:
            from_date = utils.get_datetime(from_date)
            to_date = utils.get_datetime(to_date)
            sql = self.read_sql_file("packet_loss/audio_2")
            params = (organization_name, from_date, to_date)
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": []}
            for data in data_list:
                temp_dict = {
                    "time": data[0],
                    "total_avail": data[1],
                    "type": data[2]
                }
                final_dict.get("result").append(temp_dict)
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def download_reports_devices(self, organization_name):
        try:
            sql = self.read_sql_file("download_reports_devices")
            params = (organization_name,)
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": []}
            for dt in data_list:
                final_dict.get("result").append(dt[0])
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def read_sql_file(self, file_name):
        try:
            sql = open(
                str(helper.get_dashboard_sql_path())
                + str(file_name)
                + ".sql"
            )
            return str(sql.read())
        except (
            ValueError, FileExistsError, FileNotFoundError
        ) as e:
            print("Error while reading a file\n", e)
