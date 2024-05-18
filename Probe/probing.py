from GoogleAPI.logging_api_handler import Logging
from GoogleAPI.monitoring_api_handler import Monitoring

from Utlis.config_handler import ConfDataType, get_config_data

from Supervise.connection_status import ConnectionStatus, ConnectionLevel

from Supervise.supervisor import SupervisingDNS
from Supervise.supervisor import SupervisingISP
from Supervise.supervisor import SupervisingGC
from Supervise.supervisor import SupervisingRouter

# from Utlis.probing import ping_ip, send_curl

class Probing():

    def __init__(self, instance, enable_logging_api = True, enable_monitoring_api = True):
        self.MonitoringClient = Monitoring(instance)
        self.LoggingClient = Logging()

        # self.user_ip_address = get_config_data(ConfDataType.ADDRESS)['host-ipv4-addres']
        self.router_ip_address = get_config_data(ConfDataType.ADDRESS)['lan-router-ipv4-address']
        self.isp_ip_address = get_config_data(ConfDataType.ADDRESS)['isp-ipv4-address']
        self.dns_ip_address = get_config_data(ConfDataType.ADDRESS)['dns-ipv4-address']

        self.InspectDNS = SupervisingDNS(self.dns_ip_address)
        self.InspectISP = SupervisingISP(self.isp_ip_address)
        self.InspectGC = SupervisingGC(instance['ip_address'])

        self.InspectRouter = SupervisingRouter(self.router_ip_address)

        self.connection_status_log_name = 'connection-status-test-bs-2'
        self.wait_for_proper_connection = False
        self.connection_status_queue = []

        self.ip_address = instance['ip_address']

        self.enable_logging_api = enable_logging_api
        self.enable_monitoring_api = enable_monitoring_api
        

    def logging(self, data, log_name):
        self.LoggingClient.send_logs(data, log_name)

    def monitoring(self, value, metric_type_name):
        return self.MonitoringClient.write_time_series(value, metric_type_name)


    def insert_connection_status_to_queue(self, log_info, level, source_ip, destination_ip):

        self.connection_status_queue.append((log_info, level, source_ip, destination_ip))
    
    def handle_connection_status_queue(self):
        if len(self.connection_status_queue):
            for x in self.connection_status_queue:
                self.logging({'log_info' : x[0], 'level_failed' : int(x[1]), 'source_ip' : x[2], 'destination_ip' : x[3] }, self.connection_status_log_name)
        
        self.connection_status_queue.clear()

    def handle_dead_connection(self):

        if self.wait_for_proper_connection: return
        
        log_info = f'Connection User-VM "{self.ip_address}" is currently dead.'

        connection_status_dns = self.InspectDNS.check_connection_dead()

        if connection_status_dns != ConnectionStatus.CONNECTION_DEAD: 
            self.insert_connection_status_to_queue(log_info = log_info, level = ConnectionLevel.USER_VM, source_ip = self.user_ip_address, destination_ip = self.ip_address)
            return
            
        log_info = f'Connection User-DNS {self.InspectDNS.ip_address} is currently dead.'

        connection_status_router = self.InspectRouter.check_connection_dead()

        if connection_status_router != ConnectionStatus.CONNECTION_DEAD: 
            self.insert_connection_status_to_queue(log_info = log_info, level = ConnectionLevel.USER_DNS, source_ip = self.user_ip_address, destination_ip = self.dns_ip_address)
            return

        log_info = f'Connection User-Router {self.InspectRouter.ip_address} is currently dead.'
        self.insert_connection_status_to_queue(log_info = log_info, level = ConnectionLevel.USER_ROUTER, source_ip = self.user_ip_address, destination_ip = self.router_ip_address)
        


    def ping_handler(self, log_name = '', metric_name = ''):
        ping_gc_data = self.InspectGC.insert_connection_data()
        ping_dns_data = self.InspectDNS.insert_connection_data()
        ping_router_data = self.InspectRouter.insert_connection_data()
        ping_isp_data = self.InspectISP.insert_connection_data()

        print(ping_gc_data)

        connection_status = self.InspectGC.check_connection_dead()

        if connection_status == ConnectionStatus.CONNECTION_DEAD: 
            self.handle_dead_connection()
            self.wait_for_proper_connection = True
            return
        
        if connection_status == ConnectionStatus.CONNECTION_CURRENTLY_FINE:
            if self.wait_for_proper_connection == True:
                self.wait_for_proper_connection = False
                self.insert_connection_status_to_queue(log_info = f'Connection User-GC working fine', level = ConnectionLevel.USER_CONNECTION_FINE_AGAIN, source_ip = self.user_ip_address, destination_ip = self.ip_address)

            self.handle_connection_status_queue()

        if self.enable_monitoring_api:
            can_send_metric = self.monitoring(ping_gc_data['avg_rtt'], metric_name)
          
            if can_send_metric:
                print('Log sent')
                if self.enable_logging_api: self.logging(ping_gc_data, log_name)
            
        


