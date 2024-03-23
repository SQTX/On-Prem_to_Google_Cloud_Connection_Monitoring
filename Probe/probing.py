from icmplib import ping

from GoogleAPI.logging_api_handler import Logging
from GoogleAPI.monitoring_api_handler import Monitoring

class Probing():

    def __init__(self, instance, enable_monitoring = True, enable_logging = True) -> None:
        self.MonitoringClient = Monitoring(instance)
        self.LoggingClient = Logging

        self.ip_address = instance['ip_address']
        
        self.enable_logging = enable_logging
        self.enable_monitoring = enable_monitoring
    
    def ping_instance(self, metric_type_name = 'example', metric_store_id = 'Pittsburgh', **kwargs):
        ping_raw = ping(address = self.ip_address, **kwargs)

        data = {'ip_address'    :         ping_raw.address,
                'min_rtt'       :         ping_raw.min_rtt,
                'max_rtt'       :         ping_raw.max_rtt,
                'avg_rtt'       :         ping_raw.avg_rtt,
                'packet_loss'   :         ping_raw.packet_loss,
                'jitter'        :         ping_raw.jitter,
                'is_alive'      :         ping_raw.is_alive}

        if self.enable_logging == True: self.LoggingClient.send_logs(data)
        if self.enable_monitoring == True: self.MonitoringClient.write_time_series()
