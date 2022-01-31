from reports.device_at_a_glance import DeviceAtAGlance
from reports.device_combo import DeviceCombo
from reports.chart_device_metrics import ChartDeviceMetrics
from reports.ssl_certificate import SSLCertificate
from reports.report_utils import ReportUtility
from reports.video_endpoint_availability import VideoEndpointAvailability
from reports.video_unavailablity import VideoUnavailablity
from reports.device_count import DeviceCount
from reports.event_detection import EventDetection
from reports.slcs_detection import SlcsDetection
from reports.device_availability import DeviceAvailability
from reports.device_utilization_metrics import DeviceUtilizationMetrics
from reports.device_uptime import DeviceUptime
from reports.asset_list import AssetList
from reports.chart_video_endpoint_avail import ChartVideoEndpointAvail
from reports.chart_video_endpoint_Unavail import ChartVideoEndpointUnAvail
from reports.chart_video_packet_loss import ChartVideoEndPointPacketLoss
from reports.chart_device_avail import DevicesAvailableChart
from reports.device_outage_history import DeviceOutageHistory
from reports.unique_events import UniqueEvents
from reports.device_vital_threshold import DeviceVitalThreshold
deviceVitalThreshold = DeviceVitalThreshold()

device_at_a_glance = DeviceAtAGlance()
device_combo = DeviceCombo()
chart_device_metrics = ChartDeviceMetrics()
unique_events = UniqueEvents()
outage_history = DeviceOutageHistory()
devices_available_chart = DevicesAvailableChart()
packet_loss = ChartVideoEndPointPacketLoss()
chart_video_endpoint = ChartVideoEndpointAvail()
chart_video_endpoint_unavail = ChartVideoEndpointUnAvail()
metrix = DeviceUtilizationMetrics()
video_endpoint = VideoEndpointAvailability()
device_count = DeviceCount()
utils = ReportUtility()
ssl = SSLCertificate()
video_unavailablity = VideoUnavailablity()
event_detection = EventDetection()
slcs = SlcsDetection()
device_availability = DeviceAvailability()
device_uptime = DeviceUptime()
asset_list = AssetList()


class ReportServices:
    def generate_reports(self, types, request, organizations, devices_by_organization):
        from_date = utils.get_datetime(request.headers.get('fromdate'))
        to_date = utils.get_datetime(request.headers.get('todate'))

        if organizations is None or str(organizations) == "" or from_date is None or str(from_date) == "" or to_date is None or str(to_date) == "":
            return "error"
        if "Video_Endpoint_Availability" in types:
            return video_endpoint.get_report(
                from_date, to_date, organizations, devices_by_organization)
        elif "device_count" in types:
            return device_count.get_report(
                from_date, to_date, organizations, devices_by_organization)
        elif "ssl_certificate" in types:
            return ssl.get_report(
                from_date, to_date, organizations, devices_by_organization)
        elif "video_unavailablity" in types:
            return video_unavailablity.get_report(
                from_date, to_date, organizations, devices_by_organization)
        elif "event_detection" in types:
            return event_detection.get_report(
                from_date, to_date, organizations, devices_by_organization)
        elif "slcs_detection" in types:
            return slcs.get_report(
                from_date, to_date, organizations, devices_by_organization)
        elif "deviceAvailability" in types:
            return device_availability.get_report(
                from_date, to_date, organizations, devices_by_organization)
        elif "device_utilization_metrics" in types:
            return metrix.get_report(
                from_date, to_date, organizations, devices_by_organization)
        elif "device_uptime" in types:
            return device_uptime.get_report(
                from_date, to_date, organizations, devices_by_organization)
        elif "asset_list" in types:
            return asset_list.get_report(
                from_date, to_date, organizations, devices_by_organization)
        elif "chart_video_endpoint_avail" in types:
            return chart_video_endpoint.get_report(
                from_date, to_date, organizations, devices_by_organization)
        elif "chart_video_endpoint_Unavail" in types:
            return chart_video_endpoint_unavail.get_report(
                from_date, to_date, organizations, devices_by_organization)
        elif "chart_packet_loss" in types:
            return packet_loss.get_report(
                from_date, to_date, organizations, devices_by_organization)
        elif "chart_device_availability" in types:
            return devices_available_chart.get_report(
                from_date, to_date, organizations, devices_by_organization)
        elif "outage_history" in types:
            return outage_history.get_report(
                from_date, to_date, organizations, devices_by_organization)
        elif "unique_events" in types:
            return unique_events.get_report(
                from_date, to_date, organizations, devices_by_organization)
        elif "device_vitalThreshold" in types:
            return deviceVitalThreshold.get_report(
                from_date, to_date, organizations, devices_by_organization)
        elif "chart_deviceMetrics" in types:
            return chart_device_metrics.get_report(
                from_date, to_date, organizations, devices_by_organization)
        elif "device_combo" in types:
            return device_combo.get_report(
                from_date, to_date, organizations, devices_by_organization)
        elif "device_at_a_glance" in types:
            return device_at_a_glance.get_report(
                from_date, to_date, organizations, devices_by_organization)
        else:
            return "error"
