from helpers import Helpers


class DashboardDownloadsSqlHelpers:
    def __init__(self):
        self._helpers = Helpers()

    def get_query(self, type, organization_name, infrastructure, video_endpoint, audio_endpoint):
        if type in "all_devices_summary":
            return self.get_summary_devices_query(organization_name)
        elif type in "infrastructure_devices_summary":
            return self.infrastructure_devices(organization_name, infrastructure)
        elif type in "video_endpoints_summary":
            return self.video_endpoints(organization_name, video_endpoint)
        elif type in "audio_endpoints_summary":
            return self.get_summary_of_audio_endpoints(organization_name, audio_endpoint)
        
        elif type in "top_10_problematic_devices_count":
            return self.problematic_devices(organization_name)
        elif type in "top_10_events_count":
            return self.device_events(organization_name)
        elif type in "top_5_infra_memory_usage":
            return self.infrastructure_memory_usage(organization_name, infrastructure)
        elif type in "top_5_infra_cpu_usage":
            return self.infrastructure_cpu_usage(organization_name, infrastructure)
        elif type in "devices_availability":
            return self.devices_availability(organization_name, infrastructure)
        elif type in "device_count_by_vendor":
            return self.devices_by_vendor_type(organization_name)
        elif type in "device_count_by_category":
            return self.devices_by_category(organization_name)
        elif type in "device_count_by_location_category":
            return self.devices_by_category_location(organization_name)
        elif type in "certificate_data":
            return self.get_certificate_data(organization_name, infrastructure)
        elif type in "scheduled_maintenance":
            return self.scheduled_maintenance(organization_name)
        elif type in "all_data_results":
            all_query_dict = {}
            all_query_dict.update(
                self.get_summary_devices_query(organization_name))
            all_query_dict.update(self.infrastructure_devices(
                organization_name, infrastructure))
            all_query_dict.update(self.video_endpoints(
                organization_name, video_endpoint))
            all_query_dict.update(self.get_summary_of_audio_endpoints(
                organization_name, audio_endpoint))
            all_query_dict.update(
                self.problematic_devices(organization_name))
            all_query_dict.update(self.device_events(organization_name))
            all_query_dict.update(self.infrastructure_memory_usage(
                organization_name, infrastructure))
            all_query_dict.update(self.infrastructure_cpu_usage(
                organization_name, infrastructure))
            all_query_dict.update(self.devices_availability(
                organization_name, infrastructure))
            all_query_dict.update(
                self.devices_by_vendor_type(organization_name))
            all_query_dict.update(
                self.devices_by_category(organization_name))
            all_query_dict.update(
                self.devices_by_category_location(organization_name))
            all_query_dict.update(self.get_certificate_data(
                organization_name, infrastructure))
            all_query_dict.update(
                self.scheduled_maintenance(organization_name))

            return all_query_dict
        else:
            return {}

    def get_summary_devices_query(self, organization_name):
        total_device_summary = self.read_sql_file(
            "all_devices/device_count")
        device_alarm_summary = self.read_sql_file(
            "all_devices/alarm_count")
        device_down_count_summary = self.read_sql_file(
            "all_devices/down_count")
        query_dict = {
            "total_device_summary": {
                "query": total_device_summary,
                "params": (organization_name,)
            },
            "device_alarm_summary": {
                "query": device_alarm_summary,
                "params": (organization_name, ('4', '3', '2', '1'))
            },
            "device_down_count_summary":  {
                "query": device_down_count_summary,
                "params": ((
                    'Device Failed Availability Check: UDP - SNMP',
                    'Device Failed Availability Check: ICMP - Ping'),
                    organization_name, ('4', '3', '2', '1')
                )
            }
        }
        return query_dict

    def infrastructure_devices(
            self, organization_name, infrastructure):
        infrastructure = str(infrastructure).strip()
        infrastructure_devices = self.read_sql_file(
            "infrastructure/device_count")
        infrastructure_alarms = self.read_sql_file(
            "infrastructure/alarm_count")
        infrastructure_down_count = self.read_sql_file(
            "infrastructure/down_count")
        query_dict = {
            "Total_Infras_Device_Summary": {
                "query": infrastructure_devices,
                "params": (infrastructure, organization_name)
            },
            "infrastructure_alarms": {
                "query": infrastructure_alarms,
                "params": (infrastructure, organization_name, ('4', '3', '2', '1'))
            },
            "Infra_Down_Count_Summary": {
                "query": infrastructure_down_count,
                "params": (infrastructure, organization_name, ('4', '3', '2', '1'))
            }
        }
        return query_dict

    def video_endpoints(
            self, organization_name, video_endpoint):
        video_endpoint = str(video_endpoint).strip()
        video_endpoints = self.read_sql_file(
            "video_endpoints/device_count")
        video_endpoints_alarms = self.read_sql_file(
            "video_endpoints/alarm_count")
        video_endpoints_down = self.read_sql_file(
            "video_endpoints/down_count")
        query_dict = {
            "video_endpoints": {
                "query": video_endpoints,
                "params": (video_endpoint, organization_name)
            },
            "video_endpoints_alarms": {
                "query": video_endpoints_alarms,
                "params": (
                    video_endpoint, organization_name,
                    ('4', '3', '2', '1'))
            },
            "video_endpoints_down": {
                "query": video_endpoints_down,
                "params": (
                    video_endpoint, organization_name,
                    ('4', '3', '2', '1'))
            }
        }
        return query_dict

    def get_summary_of_audio_endpoints(
            self, organization_name, audio_endpoint):
        audio_endpoint = str(audio_endpoint).strip()
        audio_endpoints = self.read_sql_file(
            "audio_endpoints/device_count")
        audio_endpoints_alarm = self.read_sql_file(
            "audio_endpoints/alarm_count")
        audio_endpoints_down_count = self.read_sql_file(
            "audio_endpoints/down_count")
        query_dict = {
            "Total_Audio_EndPoints_Summary": {
                "query": audio_endpoints,
                "params": (audio_endpoint, organization_name)
            },
            "Audio_EndPoints_Alarms_Summary": {
                "query": audio_endpoints_alarm,
                "params": (
                    audio_endpoint, organization_name,
                    ('4', '3', '2', '1'))
            },
            "Audio_EndPoints_Count_Summary": {
                "query": audio_endpoints_down_count,
                "params": (
                    audio_endpoint, organization_name,
                    ('4', '3', '2', '1'))
            }
        }
        return query_dict

    def problematic_devices(self, organization_name):
        problematic_devices = self.read_sql_file(
            "top/10/problematic_devices")
        query_dict = {
            "problematic_devices": {
                "query": problematic_devices,
                "params": (organization_name, organization_name)
            }
        }
        return query_dict

    def device_events(self, organization_name):
        device_events = self.read_sql_file(
            "top/10/event_count")
        query_dict = {
            "Device_Events": {
                "query": device_events,
                "params": (organization_name, organization_name)
            }
        }
        return query_dict

    def infrastructure_memory_usage(
            self, organization_name, infrastructure):
        infra_memory_utilization = self.read_sql_file(
            "top/5/memory_usage")
        query_dict = {
            "Infra_Memory_Utilization": {
                "query": infra_memory_utilization,
                "params": (organization_name, infrastructure)
            }
        }
        return query_dict

    def infrastructure_cpu_usage(
            self, organization_name, infrastructure):
        infra_cpu_utilization = self.read_sql_file(
            "top/5/cpu_usage")
        query_dict = {
            "Infra_CPU_Utilization": {
                "query": infra_cpu_utilization,
                "params": (organization_name, infrastructure)
            }
        }
        return query_dict

    def devices_availability(
            self, organization_name, infrastructure):
        infrastructure = str(infrastructure).strip()
        device_availability_excluding_infrastructure = self.read_sql_file(
            "availability/all_devices_excluding_infrastructure")
        infrastructure_device_availability = self.read_sql_file(
            "availability/infrastructure_devices")
        query_dict = {
            "Availability_Excluding_Infr": {
                "query": device_availability_excluding_infrastructure,
                "params": (organization_name, infrastructure)},
            "Availability_Infra_Devices": {
                "query": infrastructure_device_availability,
                "params": (infrastructure, organization_name)
            }
        }
        return query_dict

    def devices_by_vendor_type(self, organization_name):
        devices_by_vendor_type = self.read_sql_file(
            "device_count_by_vendor")
        query_dict = {
            "Devices_By_Vendor_Type": {
                "query": devices_by_vendor_type,
                "params": (organization_name,)
            },
        }
        return query_dict

    def devices_by_category(self, organization_name):
        devices_by_category = self.read_sql_file(
            "device_count_by_category")
        query_dict = {
            "Devices_By_Category": {
                "query": devices_by_category,
                "params": (organization_name,)
            },
        }
        return query_dict

    def devices_by_category_location(self, organization_name):
        devices_by_category_location = self.read_sql_file(
            "device_count_by_location_category")
        query_dict = {
            "Devices_by_CategoryLocation": {
                "query": devices_by_category_location,
                "params": (organization_name,)
            },
        }
        return query_dict

    def get_certificate_data(
            self, organization_name, infrastructure):
        infrastructure = str(infrastructure).strip()
        certificate_data = self.read_sql_file(
            "certificate_expiration")
        query_dict = {
            "certificate_data": {
                "query": certificate_data,
                "params": (infrastructure, organization_name)
            },
        }
        return query_dict

    def scheduled_maintenance(self, organization_name):
        scheduled_maintenance_table = self.read_sql_file(
            "scheduled_maintenance")
        query_dict = {
            "Scheduled_Maintenance_Table": {
                "query": scheduled_maintenance_table,
                "params": (organization_name,)
            },
        }
        return query_dict

    def read_sql_file(self, file_name):
        try:
            sql = open(
                str(self._helpers.get_download_queries())
                + str(file_name)
                + ".sql"
            )
            return sql.read()
        except (
            ValueError, FileExistsError, FileNotFoundError
        ) as e:
            print("Error while reading a file\n", e)
