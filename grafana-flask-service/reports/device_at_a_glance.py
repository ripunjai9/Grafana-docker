from reports.device_at_a_glance_chart import DeviceAtAGlanceChart
from reports.report_utils import ReportUtility
from sciencelogic_db import ScienceLogicDb

utils = ReportUtility()
xls = DeviceAtAGlanceChart()


class DeviceAtAGlance:
    def __init__(self):
        self.sciencelogic_db = ScienceLogicDb()

    def get_report(self, from_date,to_date,organizations,device_name):

        final = self.generate_report(from_date, to_date, organizations,device_name)
        return xls.write_data_xls(final, from_date, to_date)

    def generate_report(self, from_date, to_date, organizations, device_name):
        query = utils.frame_query("device_at_a_glance")
        final = {}
        count = 0
        mem_dict = {}
        cpu_dict = {}
        swap_dict = {}
        avail_dict = {}
        schedule_dict = {}
        unschedule_dict = {}

        for innser_query in query.split("===next==="):
            if count < 4:
                params = ( from_date, to_date, organizations, device_name, )
            else:
                params = (device_name,from_date, to_date, from_date, to_date,)
            data = self.sciencelogic_db.execute(innser_query, params, True)
            headr = data[0]
            data.pop(0)
            count += 1
            for v in data:
                did = v[0]
                # temp = []
                if 'avg(nh.avg_data) AS "CPU %% AVG"' in innser_query:
                    if cpu_dict.get(did) is None:
                        temp = [round(float(v[2]), 2), round(float(v[3]), 2), round(float(v[4]), 2)]
                        cpu_dict[did] = temp
                    else:
                        temp = [round(float(v[2]), 2), round(float(v[3]), 2), round(float(v[4]), 2)]
                        cpu_dict.get(did).extend(temp)
                elif 'avg(nh.avg_data) AS "Mem %% AVG"' in innser_query:
                    if mem_dict.get(did) is None:
                        temp = [round(float(v[2]), 2), round(float(v[3]), 2), round(float(v[4]), 2)]
                        mem_dict[did] = temp
                    else:
                        temp = [round(float(v[2]), 2), round(float(v[3]), 2), round(float(v[4]), 2)]
                        mem_dict.get(did).extend(temp)
                elif "MAX(nh.max_data) AS 'Swap %% MAX'" in innser_query:
                    if swap_dict.get(did) is None:
                        temp = [round(float(v[2]), 2), round(float(v[3]), 2), round(float(v[4]), 2)]
                        swap_dict[did] = temp
                    else:
                        temp = [round(float(v[2]), 2), round(float(v[3]), 2), round(float(v[4]), 2)]
                        swap_dict.get(did).extend(temp)

                elif 'avg(avg_d_check) * 100 AS Availability' in innser_query:
                    if avail_dict.get(did) is None:
                        temp = [round(float(v[2]),2), round(100-float(v[2]), 2)]
                        avail_dict[did] = temp
                    else:
                        temp = [round(float(v[2]), 2), round(100 - float(v[2]), 2)]
                        avail_dict.get(did).extend(temp)

                elif 'Scheduled_outage_Count' in innser_query:
                    # temp = [int(v[2])]
                    if schedule_dict.get(did) is None:
                        # final[did] = [[], [], [], [], temp]
                        temp = [v[2], v[3]]
                        schedule_dict[did] = [temp]
                    else:
                        temp = [v[2], v[3]]


                        schedule_dict.get(did).append(temp)
                elif 'Unscheduled_outage_Count' in innser_query:
                    # temp = [int(v[2])]
                    if unschedule_dict.get(did) is None:
                        temp = [v[2], v[3]]
                        unschedule_dict[did] = [temp]
                    else:
                        temp = [v[2], v[3]]
                        unschedule_dict.get(did).append(temp)
        device_names = device_name #.replace("(", "").replace(")", "").replace("'", "").split(',')
        # final = device_info_dict
        # print('cpu_dict', cpu_dict)
        for key in device_names:
            final[key] = []
        for v in final.keys():
            temp_list = []
            cpu_list = cpu_dict.get(v)

            if cpu_dict.get(v) is not None:
                # print(cpu_list)
                temp_list.append(cpu_list)
            else:
                # print(cpu_list, v)
                temp_list.append([])
            mem_list = mem_dict.get(v)
            if mem_dict.get(v) is not None:
                temp_list.append(mem_list)
            else:
                temp_list.append([])
            swap_list = swap_dict.get(v)
            if swap_dict.get(v) is not None:
                temp_list.append(swap_list)
                # print(v)
            else:
                temp_list.append([])

            avail_list = avail_dict.get(v)
            if avail_dict.get(v) is not None:
                temp_list.append(avail_list)
            else:
                temp_list.append([])

            schedule_list = schedule_dict.get(v)
            if schedule_dict.get(v) is not None:
                temp_list.append(schedule_list)
            else:
                temp_list.append([])

            unschedule_list = unschedule_dict.get(v)
            if unschedule_dict.get(v) is not None:
                temp_list.append(unschedule_list)
            else:
                temp_list.append([])

            final[v] = temp_list

        return final

