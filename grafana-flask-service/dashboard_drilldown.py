from sciencelogic_db import ScienceLogicDb
from helpers import Helpers

helpers = Helpers()


class DashboardDrilldown:
    def __init__(self):
        self.sciencelogic_db = ScienceLogicDb()

    def get_query(self, type, organization_name, infrastructure, Video_End_Point, audio_endpoint):

        if type in "all_devices":
            return self.device_count(organization_name)
        elif type in "all_alarm_devices":
            return self.devices_alarm_count(organization_name)
        elif type in "summary_of_all_down_devices":
            return self.devices_down_count(organization_name)

        elif type in "infrastructure_devices":
            return self.infrastructure_device_count(organization_name, infrastructure)
        elif type in "infrastructure_alarm_devices":
            return self.infrastructure_device_alarm_count(organization_name, infrastructure)
        elif type in "infrastructure_down_devices":
            return self.infrastructure_device_down_count(organization_name, infrastructure)

        elif type in "video_endpoints":
            return self.video_endpoints_device_count(organization_name, Video_End_Point)
        elif type in "video_endpoints_alarm_devices":
            return self.video_endpoints_alarm_count(organization_name, Video_End_Point)
        elif type in "video_endpoints_down_devices":
            return self.video_endpoints_down_count(organization_name, Video_End_Point)

        elif type in "audio_endpoints":
            return self.audio_endpoints_device_count(organization_name, audio_endpoint)
        elif type in "audio_endpoints_alarm_devices":
            return self.audio_endpoints_alarm_count(organization_name, audio_endpoint)
        elif type in "audio_endpoints_down_devices":
            return self.audio_endpoints_down_count(organization_name, audio_endpoint)

        elif type in "top_10_events_count":
            return self.top_10_device_count(organization_name)
        elif type in "top_10_problematic_devices_count":
            return self.top_10_problematic_devices(organization_name)

        elif type in "device__count_by_vendor":
            return self.vendor_device_count(organization_name)
        elif type in "top_5_infra_memory_usage":
            return self.top_memory_usage(organization_name, infrastructure)
        elif type in "top_5_infra_cpu_usage":
            return self.top_cpu_usage(organization_name, infrastructure)

        elif type in "all_availability_devices_excluding_infrastructure":
            return self.all_devices_excluding_infrastructure(organization_name, infrastructure)
        elif type in "all_infrastructure_device_availability":
            return self.all_devices_including_infrastructure(organization_name, infrastructure)

        elif type in "device_count_by_category":
            return self.category_device_count_dashboard(organization_name)
        elif type in "device_count_by_location_category":
            return self.device_count_by_location_category(organization_name)
        elif type in "certificate_expiration":
            return self.certificate_expiration(organization_name, infrastructure)

        # elif type in "device_port_utilization_percentage":
        #     return self.device_port_usage_percentage(organization_name, infrastructure)
        # elif type in "device_license_utilization_percentage":
        #     return self.device_license_usage_percentage(organization_name, infrastructure)
        # elif type in "top_end_point_packet_loss":
        #     return self.top_end_point_packet_loss(organization_name)
        elif type in "scheduled_maintenance":
            return self.scheduled_maintenance_table(organization_name)
        else:
            return {}

    def device_count(self, organization_name):
        try:
            sql = self.read_sql_file("all_devices/device_count")
            params = (organization_name,)
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": []}
            for data in data_list:
                temp_dict = {
                    "organization": data[0],
                    "device_name": data[1],
                    "ip": data[2],
                    "device_category": data[3],
                    "device_type": data[4],
                    "device_class": data[5],
                    "device_location": data[6],
                    "vendor": data[7],
                }
                final_dict.get("result").append(temp_dict)
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def devices_alarm_count(self, organizations):
        try:
            sql = self.read_sql_file("all_devices/alarm_count")
            params = (organizations,)
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": []}
            for data in data_list:
                temp_dict = {
                    "organization": data[0],
                    "device_name": data[1],
                    "ip": data[2],
                    "device_category": data[3],
                    "device_type": data[4],
                    "device_class": data[5],
                    "device_location": data[6],
                    "vendor": data[7],
                    "event_message": data[8],
                    "severity": data[9],
                    "last_detected": data[10],
                }
                final_dict.get("result").append(temp_dict)
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def devices_down_count(self, organizations):
        try:
            sql = self.read_sql_file("all_devices/down_count")
            params = (organizations,)
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": []}
            for data in data_list:
                temp_dict = {
                    "organization": data[0],
                    "device_name": data[1],
                    "ip": data[2],
                    "device_category": data[3],
                    "device_type": data[4],
                    "device_class": data[5],
                    "device_location": data[6],
                    "vendor": data[7],
                    "event_message": data[8],
                    "severity": data[9],
                    "last_detected": data[10],
                }
                final_dict.get("result").append(temp_dict)
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def infrastructure_device_count(self, organizations, infrastructure):
        try:
            sql = self.read_sql_file("infrastructure/device_count")
            params = (organizations, str(infrastructure))
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": []}
            for data in data_list:
                temp_dict = {                    
                    "organization": data[0],
                    "device_name": data[1],
                    "ip": data[2],
                    "device_category": data[3],
                    "device_type": data[4],
                    "device_class": data[5],
                    "device_location": data[6],
                    "vendor": data[7],
                }
                final_dict.get("result").append(temp_dict)
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def infrastructure_device_alarm_count(self, organizations, infrastructure):
        try:
            sql = self.read_sql_file("infrastructure/alarm_count")
            params = (organizations, str(infrastructure))
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": []}
            for data in data_list:
                temp_dict = {
                    "organization": data[0],
                    "device_name": data[1],
                    "ip": data[2],
                    "device_category": data[3],
                    "device_type": data[4],
                    "device_class": data[5],
                    "device_location": data[6],
                    "vendor": data[7],
                    "event_message": data[8],
                    "severity": data[9],
                    "last_detected": data[10],
                }
                final_dict.get("result").append(temp_dict)
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def infrastructure_device_down_count(self, organizations, infrastructure):
        try:
            sql = self.read_sql_file("infrastructure/down_count")
            params = (organizations, str(infrastructure))
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": []}
            for data in data_list:
                temp_dict = {
                    "organization": data[0],
                    "device_name": data[1],
                    "ip": data[2],
                    "device_category": data[3],
                    "device_type": data[4],
                    "device_class": data[5],
                    "device_location": data[6],
                    "vendor": data[7],
                    "event_message": data[8],
                    "severity": data[9],
                    "last_detected": data[10],
                }
                final_dict.get("result").append(temp_dict)
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def video_endpoints_device_count(self, organizations, Video_End_Point):
        try:
            sql = self.read_sql_file("video_endpoints/device_count")
            params = (organizations, str(Video_End_Point))
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": []}
            for data in data_list:
                temp_dict = {
                    "organization": data[0],
                    "device_name": data[1],
                    "ip": data[2],
                    "device_category": data[3],
                    "device_type": data[4],
                    "device_class": data[5],
                    "device_location": data[6],
                    "vendor": data[7],
                }
                final_dict.get("result").append(temp_dict)
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def video_endpoints_alarm_count(self, organization_name, Video_End_Point):
        try:
            sql = self.read_sql_file("video_endpoints/alarm_count")
            params = (organization_name, str(Video_End_Point))
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": []}
            for data in data_list:
                temp_dict = {
                    "organization": data[0],
                    "device_name": data[1],
                    "ip": data[2],
                    "device_category": data[3],
                    "device_type": data[4],
                    "device_class": data[5],
                    "device_location": data[6],
                    "vendor": data[7],
                    "event_message": data[8],
                    "severity": data[9],
                    "last_detected": data[10],
                }
                final_dict.get("result").append(temp_dict)
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def video_endpoints_down_count(self, organization_name, Video_End_Point):
        try:
            sql = self.read_sql_file("video_endpoints/down_count")
            params = (organization_name, str(Video_End_Point))
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": []}
            for data in data_list:
                temp_dict = {
                    "organization": data[0],
                    "device_name": data[1],
                    "ip": data[2],
                    "device_category": data[3],
                    "device_type": data[4],
                    "device_class": data[5],
                    "device_location": data[6],
                    "vendor": data[7],
                    "event_message": data[8],
                    "severity": data[9],
                    "last_detected": data[10],
                }
                final_dict.get("result").append(temp_dict)
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def audio_endpoints_device_count(self, organization_name, audio_endpoint):
        try:
            sql = self.read_sql_file("audio_endpoints/device_count")
            params = (organization_name, str(audio_endpoint))
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": []}
            for data in data_list:
                temp_dict = {
                    "organization": data[0],
                    "device_name": data[1],
                    "ip": data[2],
                    "device_category": data[3],
                    "device_type": data[4],
                    "device_class": data[5],
                    "device_location": data[6],
                    "vendor": data[7],
                }
                final_dict.get("result").append(temp_dict)
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def audio_endpoints_alarm_count(self, organization_name, audio_endpoint):
        try:
            sql = self.read_sql_file("audio_endpoints/alarm_count")
            params = (organization_name, str(audio_endpoint))
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": []}
            for data in data_list:
                temp_dict = {
                    "organization": data[0],
                    "device_name": data[1],
                    "ip": data[2],
                    "device_category": data[3],
                    "device_type": data[4],
                    "device_class": data[5],
                    "device_location": data[6],
                    "vendor": data[7],
                    "event_message": data[8],
                    "severity": data[9],
                    "last_detected": data[10],
                }
                final_dict.get("result").append(temp_dict)
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def audio_endpoints_down_count(self, organization_name, audio_endpoint):
        try:
            sql = self.read_sql_file("audio_endpoints/down_count")
            params = (organization_name, str(audio_endpoint))
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": []}
            for data in data_list:
                temp_dict = {
                    "organization": data[0],
                    "device_name": data[1],
                    "ip": data[2],
                    "device_category": data[3],
                    "device_type": data[4],
                    "device_class": data[5],
                    "device_location": data[6],
                    "vendor": data[7],
                    "event_message": data[8],
                    "severity": data[9],
                    "last_detected": data[10],
                }
                final_dict.get("result").append(temp_dict)
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def top_10_problematic_devices(self, organization_name):
        try:
            sql = self.read_sql_file("top/10/problematic_devices")
            params = (organization_name, organization_name)
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": []}
            for data in data_list:
                temp_dict = {
                    "organization": data[0],
                    "device_name": data[1],
                    "ip": data[2],
                    "device_category": data[3],
                    "device_type": data[4],
                    "device_class": data[5],
                    "device_location": data[6],
                    "vendor": data[7],
                    "event_message": data[8],
                    "severity": data[9],
                    "last_detected": data[10],
                }
                final_dict.get("result").append(temp_dict)
            return final_dict
        except Exception as e:
            print(e)
            return {}

    def top_10_device_count(self, organization_name):
        try:
            sql = self.read_sql_file("top/10/event_count")
            params = (organization_name, organization_name)
            data_list = self.sciencelogic_db.execute(sql, params)
            final_dict = {"result": []}
            for data in data_list:
                temp_dict = {
                    "organization": data[0],
                    "device_name": data[1],
                    "ip": data[2],
                    "device_category": data[3],
                    "device_type": data[4],
                    "device_class": data[5],
                    "device_location": data[6],
                    "vendor": data[7],
                    "event_message": data[8],
                    "severity": data[9],
                    "last_detected": data[10],
                }
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
            for data in data_list:
                temp_dict = {
                    "organization": data[0],
                    "device_name": data[1],
                    "ip": data[2],
                    "device_category": data[3],
                    "device_type": data[4],
                    "device_class": data[5],
                    "device_location": data[6],
                    "vendor": data[7],
                }
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
            for data in data_list:
                temp_dict = {
                    "organization": data[0],
                    "device_name": data[1],
                    "ip": data[2],
                    "device_category": data[3],
                    "device_type": data[4],
                    "device_class": data[5],
                    "device_location": data[6],
                    "vendor": data[7],
                    "device_Availability": str(data[8])+'%',
                }
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
            for data in data_list:
                temp_dict = {
                    "organization": data[0],
                    "device_name": data[1],
                    "ip": data[2],
                    "device_category": data[3],
                    "device_type": data[4],
                    "device_class": data[5],
                    "device_location": data[6],
                    "vendor": data[7],
                    "device_Availability": str(data[8]) + '%',
                }
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
            for data in data_list:
                temp_dict = {
                    "organization": data[0],
                    "device_name": data[1],
                    "ip": data[2],
                    "device_category": data[3],
                    "device_type": data[4],
                    "device_class": data[5],
                    "device_location": data[6],
                    "vendor": data[7],
                    "memory_utilization_value": data[8] + '%',
                }
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
            for data in data_list:
                temp_dict = {
                    "organization": data[0],
                    "device_name": data[1],
                    "ip": data[2],
                    "device_category": data[3],
                    "device_type": data[4],
                    "device_class": data[5],
                    "device_location": data[6],
                    "vendor": data[7],
                    "CPU_utilization_value": data[8] + '%',
                }
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
            for data in data_list:
                temp_dict = {
                    "organization": data[0],
                    "device_name": data[1],
                    "ip": data[2],
                    "device_category": data[3],
                    "device_type": data[4],
                    "device_class": data[5],
                    "device_location": data[6],
                    "vendor": data[7],
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
                    "organization": data[0],
                    "device_name": data[1],
                    "ip": data[2],
                    "device_category": data[3],
                    "device_type": data[4],
                    "device_class": data[5],
                    "device_location": data[6],
                    "vendor": data[7],
                    "certificate_organization": data[8],
                    "cert_id": data[9],
                    "expiration_date": data[10],
                    "days_left": data[11],
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
                    "organization": data[0],
                    "device_name": data[1],
                    "ip": data[2],
                    "device_category": data[3],
                    "device_type": data[4],
                    "device_class": data[5],
                    "device_location": data[6],
                    "vendor": data[7],
                    "schedule_summary": data[8],
                    "schedule_description": data[9],
                    "schedule_start_date": data[10],
                    "schedule_end_date": data[11]
                }
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
                    "organization": data[0],
                    "device_name": data[1],
                    "ip": data[2],
                    "device_category": data[3],
                    "device_type": data[4],
                    "device_class": data[5],
                    "device_location": data[6],
                    "vendor": data[7],
                }
                final_dict.get("result").append(temp_dict)
            return final_dict
        except Exception as e:
            print(e)
            return {}


    # def device_port_usage_percentage(self, organization_name, infrastructure):
    #     try:
    #         f = open(helpers.get_dashboard_query_path() +
    #                  "device_port_utilization_percentage.sql", "r")
    #         sql = str(f.read())
    #         params = (organization_name, infrastructure)
    #         data_list = self.sciencelogic_db.execute(sql, params)
    #         final_dict = {"result": []}
    #         count = 0
    #         for data in data_list:
    #             temp_dict = {
    #                 "time": data[0],
    #                 "device": data[1],
    #                 "average": data[2]
    #             }
    #             count += 1
    #             final_dict.get("result").append(temp_dict)
    #         if count < 5:
    #             while True:
    #                 if count == 5:
    #                     break
    #                 temp_dict = {
    #                     "time": "-1",
    #                     "device": ".",
    #                     "average": "0"
    #                 }
    #                 count += 1
    #                 final_dict.get("result").append(temp_dict)
    #         return final_dict
    #     except Exception as e:
    #         print(e)
    #         return {}

    # def device_license_usage_percentage(self, organization_name, infrastructure):
    #     try:
    #         f = open(helpers.get_dashboard_query_path() +
    #                  "device_license_utilization_percentage.sql", "r")
    #         sql = str(f.read())
    #         params = (organization_name, infrastructure)
    #         data_list = self.sciencelogic_db.execute(sql, params)
    #         final_dict = {"result": []}
    #         count = 0
    #         for data in data_list:
    #             temp_dict = {
    #                 "time": data[0],
    #                 "device": data[1],
    #                 "average": data[2]
    #             }
    #             count += 1
    #             final_dict.get("result").append(temp_dict)
    #         if count < 5:
    #             while True:
    #                 if count == 5:
    #                     break
    #                 temp_dict = {
    #                     "time": "-1",
    #                     "device": ".",
    #                     "average": "0"
    #                 }
    #                 count += 1
    #                 final_dict.get("result").append(temp_dict)
    #         return final_dict
    #     except Exception as e:
    #         print(e)
    #         return {}

    # def top_end_point_packet_loss(self, organization_name):
    #     try:
    #         f = open(helpers.get_dashboard_query_path() +
    #                  "top_end_point_packet_loss.sql", "r")
    #         query = str(f.read())
    #         params = (organization_name,)
    #         data_list = self.sciencelogic_db.execute(query, params)
    #         final_dict = {"result": []}
    #         for data in data_list:
    #             temp_dict = {
    #                 "time": data[0],
    #                 "device": data[1],
    #                 "average": data[2]
    #             }
    #             final_dict.get("result").append(temp_dict)
    #         return final_dict
    #     except Exception as e:
    #         print(e)
    #         return {}

    def read_sql_file(self, file_name):
        try:
            sql = open(
                str(helpers.get_drilldown_dashboard_query_path())
                + str(file_name)
                + ".sql", "r"
            )
            return str(sql.read())
        except (
            ValueError, FileExistsError, FileNotFoundError
        ) as e:
            print("Error while reading a file\n", e)
