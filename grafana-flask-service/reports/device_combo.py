from reports.report_device_combo import ReportXls
from sciencelogic_db import ScienceLogicDb
from reports.report_utils import ReportUtility


utils = ReportUtility()
xls = ReportXls()


class DeviceCombo:
    def __init__(self):
        self.sciencelogic_db = ScienceLogicDb()

    def get_report(self, from_date, to_date, organizations, device_name):
        final, header = self.generate_report(
            from_date, to_date, organizations, device_name)

        return xls.write_data_xls(final, header, from_date, to_date)

    def generate_report(self, from_date, to_date, organizations, device_name):
        query = utils.frame_query("device_combo")
        headers = ['id']
        final_dict = {
            "report_device_combo": headers
        }
        final = {}
        count = 0
        device_info_dict = {}
        ram_dict = {}
        cpu_dict = {}
        SWAP_dict = {}
        avail_dict = {}
        port = {}
        assert_dict = {}
        fs_dict = {}
        cpu_util_dict = {}
        availb_dict2 = {}
        mem_dict = {}
        swap_min_dict = {}
        for innser_query in query.split("===next==="):

            if count in [0, 5, 6, 7]:
                params = (device_name, )
            elif count in [1, 2, 3, 4, 8, 9, 10, 11]:
                params = (organizations, device_name, from_date, to_date, )
            else:
                params = (organizations, device_name,)
            count += 1
            data = self.sciencelogic_db.execute(innser_query, params, True)
            header = data[0]
            header.pop(0)
            headers.extend(header)
            data.pop(0)

            for v in data:
                did = v[0]
                if "dca.cat_name as Device_Category" in innser_query:
                    if device_info_dict.get(did) is None:
                        temp = [v[0], v[2], v[3], v[4], v[5],
                                v[6], v[7], v[8], v[9], v[10], v[1]]

                        device_info_dict[did] = temp
                    else:
                        temp = [v[0], v[2], v[3], v[4], v[5],
                                v[6], v[7], v[8], v[9], v[10], v[1]]
                        device_info_dict.get(did).extend(temp)
                elif '"RAM %% Used"' in innser_query:
                    if ram_dict.get(did) is None:
                        ram_dict[did] = [v[1], v[2]]
                    else:
                        temp = [v[1], v[2]]
                        ram_dict.get(did).extend(temp)
                elif '"SWAP %% Used"' in innser_query:
                    if SWAP_dict.get(did) is None:
                        SWAP_dict[did] = [v[1], v[2]]
                    else:
                        temp = [v[1], v[2]]
                        SWAP_dict.get(did).extend(temp)
                elif '"CPU %% Used"' in innser_query:
                    if cpu_dict.get(did) is None:
                        cpu_dict[did] = [v[1], v[2]]
                    else:
                        temp = [v[1], v[2]]
                        cpu_dict.get(did).extend(temp)

                elif 'avg(nd.avg_d_check) * 100 as ' in innser_query:
                    if avail_dict.get(did) is None:
                        avail_dict[did] = [v[1], v[2]]
                    else:
                        temp = [v[1], v[2]]
                        avail_dict.get(did).extend(temp)

                elif "md.port_num as open_ports" in innser_query:
                    if port.get(did) is None:
                        temp = [v[1]]
                        port[did] = temp
                    else:
                        temp = [v[1]]
                        port.get(did).extend(temp)

                elif "ac.array_size as disk_array_siz" in innser_query:
                    if assert_dict.get(did) is None:
                        temp = [v[1], v[2], v[3], v[4], v[5], v[6], v[7],
                                v[8], v[9], v[10], v[11], v[12], v[13], v[14], v[15]]

                        assert_dict[did] = temp
                    else:
                        temp = [v[1], v[2], v[3], v[4], v[5], v[6], v[7],
                                v[8], v[9], v[10], v[11], v[12], v[13], v[14], v[15]]
                        assert_dict.get(did).extend(temp)
                elif "File_system" in innser_query:
                    if fs_dict.get(did) is None:
                        temp = [v[1], v[2], v[3], v[4], v[5]]

                        fs_dict[did] = [temp]
                    else:
                        temp = [v[1], v[2], v[3], v[4], v[5]]
                        fs_dict.get(did).append(temp)

                elif 'avg(nh.avg_data) AS "CPU% AVG"' in innser_query:
                    if cpu_util_dict.get(did) is None:
                        temp = [v[1], v[2]]
                        cpu_util_dict[did] = [temp]
                    else:
                        temp = [v[1], v[2]]
                        cpu_util_dict.get(did).append(temp)

                elif "avg(avg_d_check)*100 as Availability_chart" in innser_query:
                    if availb_dict2.get(did) is None:
                        temp = [v[1], v[2]]
                        availb_dict2[did] = [temp]

                    else:
                        temp = [v[1], v[2]]
                        availb_dict2.get(did).append(temp)

                elif 'avg(nh.avg_data) AS "Mem % AVG"' in innser_query:
                    if swap_min_dict.get(did) is None:
                        temp = [v[1], v[2]]
                        swap_min_dict[did] = [temp]
                    else:
                        temp = [v[1], v[2]]
                        swap_min_dict.get(did).append(temp)
                else:
                    if mem_dict.get(did) is None:
                        temp = [v[1], v[2]]
                        mem_dict[did] = [temp]
                    else:
                        temp = [v[1], v[2]]
                        mem_dict.get(did).append(temp)

        # .replace("(", "").replace(")", "").replace("'", "").split(',')
        x = device_name
        # final = device_info_dict
        for key in x:
            final[key] = []

        for v in final.keys():
            temp_list = []
            # final_lst = final.get(v)
            # temp_list.append(final_lst)
            dev_list = device_info_dict.get(v)
            if dev_list is not None:
                temp_list.append(dev_list)
            else:
                temp_list.append([])

            ram_list = ram_dict.get(v)
            if ram_dict.get(v) is not None:
                temp_list.append(ram_list)
            else:
                temp_list.append([])

            cpu_list = cpu_dict.get(v)
            if cpu_dict.get(v) is not None:
                temp_list.append(cpu_list)
            else:
                temp_list.append([])

            swap_list = SWAP_dict.get(v)
            if SWAP_dict.get(v) is not None:
                temp_list.append(swap_list)
                # print(v)

            else:
                temp_list.append([])

            avail_list = avail_dict.get(v)
            if avail_dict.get(v) is not None:
                temp_list.append(avail_list)
            else:
                temp_list.append([])

            port_list = port.get(v)

            if port.get(v) is not None:
                temp_list.append(port_list)
            else:
                temp_list.append([])

            assert_list = assert_dict.get(v)
            if assert_dict.get(v) is not None:
                temp_list.append(assert_list)
            else:
                temp_list.append([])

            fs_list = fs_dict.get(v)
            if fs_dict.get(v) is not None:
                temp_list.append(fs_list)
            else:
                temp_list.append([])
            cpu_util_list = cpu_util_dict.get(v)
            if cpu_util_dict.get(v) is not None:
                temp_list.append(cpu_util_list)
            else:
                temp_list.append([])
            avail_list2 = availb_dict2.get(v)
            if availb_dict2.get(v) is not None:
                temp_list.append(avail_list2)
            else:
                temp_list.append([])
            mem_list = mem_dict.get(v)
            if mem_dict.get(v) is not None:
                temp_list.append(mem_list)
            else:
                temp_list.append([])
            # print(swap_min_dict)
            swap_min_list = swap_min_dict.get(v)
            if swap_min_dict.get(v) is not None:
                temp_list.append(swap_min_list)
            else:
                temp_list.append([])

            final[v] = temp_list

        # print(final)
        return final, final_dict

