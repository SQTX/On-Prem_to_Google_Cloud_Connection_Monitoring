from GoogleAPI.logging_api_handler import Logging
from GoogleAPI.monitoring_api_handler import Monitoring

from Utlis.config_handler import ConfDataType, get_config_data
from Utlis.probing import print_ping_data

from Supervise.connection_status import ConnectionStatus, ConnectionLevel

from Supervise.supervisor import SupervisingDNS
from Supervise.supervisor import SupervisingISP
from Supervise.supervisor import SupervisingGC
from Supervise.supervisor import SupervisingRouter

from Alert.mail_alert_sys import send_alert_mail
import os

credential_path="Key//key.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
# from Utlis.probing import ping_ip, send_curl


#  """
#     A class used to handle probing operations including monitoring and logging of network connections.

#     Initializes the monitoring and logging clients, retrieves IP addresses from the configuration,
#     and sets up various supervision instances.
# """
class Probing():


    #     """
    # Initializes the monitoring and logging clients, retrieves IP addresses from the configuration,
    # and sets up various supervision instances.

    # Args:
    #     instance (dict): A dictionary containing instance-specific information, such as IP address.
    #     enable_logging_api (bool, optional): Flag to enable or disable the logging API. Defaults to True.
    #     enable_monitoring_api (bool, optional): Flag to enable or disable the monitoring API. Defaults to True.
        
    # Attributes:
    #     MonitoringClient (Monitoring): Client for monitoring operations.
    #     LoggingClient (Logging): Client for logging operations.
    #     router_ip_address (str): IP address of the LAN router.
    #     isp_ip_address (str): IP address of the ISP.
    #     dns_ip_address (str): IP address of the DNS server.
    #     InspectDNS (SupervisingDNS): Supervising instance for the DNS server.
    #     InspectISP (SupervisingISP): Supervising instance for the ISP.
    #     InspectGC (SupervisingGC): Supervising instance for Google Cloud using the instance's IP address.
    #     InspectRouter (SupervisingRouter): Supervising instance for the LAN router.
    #     connection_status_log_name (str): Name of the log for connection status.
    #     wait_for_proper_connection (bool): Flag to indicate waiting for a proper connection.
    #     connection_status_queue (list): Queue to hold connection status information.
    #     ip_address (str): IP address of the instance.
    #     enable_logging_api (bool): Indicates if the logging API is enabled.
    #     enable_monitoring_api (bool): Indicates if the monitoring API is enabled.
    # """
        
    def __init__(self, instance, enable_logging_api = True, enable_monitoring_api = True):
        self.MonitoringClient = Monitoring(instance)
        self.LoggingClient = Logging()

        self.user_ip_address = get_config_data(ConfDataType.ADDRESS)['host-ipv4-address']
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


    #     """
    # Sends log data to the logging client.

    # Args:
    #     data (dict): The data to be logged.
    #     log_name (str): The name of the log.
    # """   

    def logging(self, data, log_name):
        self.LoggingClient.send_logs(data, log_name)

    
    # """
    # Writes time series data to the monitoring client.

    # Args: 
    #     value (float): The value to be monitored.
    #     metric_type_name (str): The name of the metric type.

    # Returns:
    #     bool: True if the time series data was successfully written, False otherwise.
    # """

    def monitoring(self, value, metric_type_name):
        return self.MonitoringClient.write_time_series(value, metric_type_name)



    #  """
    # Inserts connection status information into the queue.

    # Args:
    #     log_info (str): Information about the log.
    #     level (int): The connection level.
    #     source_ip (str): The source IP address.
    #     destination_ip (str): The destination IP address.
    # """

    def insert_connection_status_to_queue(self, log_info, level, source_ip, destination_ip):

        self.connection_status_queue.append((log_info, level, source_ip, destination_ip))
    

    #   """
    # Handles the connection status queue by logging the information and clearing the queue.
    # """
    def handle_connection_status_queue(self):
        if len(self.connection_status_queue):
            for x in self.connection_status_queue:
                try: 
                    send_alert_mail(body = x[0])
                    print('[INFO] Mail sent')
                except Exception as e:
                    print('-' * 7, '[INFO] Cannot write log mail.', '-' * 7)
                    print(e)
                    print('-' * 30)
                    
                self.logging({'log_info' : x[0], 'level_failed' : int(x[1]), 'source_ip' : x[2], 'destination_ip' : x[3] }, self.connection_status_log_name)
        
        self.connection_status_queue.clear()


    # """
    # Handles scenarios where the connection is detected to be dead. Inserts relevant
    # connection status information into the queue and logs the status if needed.
    # """
    def handle_dead_connection(self):

        if self.wait_for_proper_connection: return
        
        log_info = f'Connection User-VM "{self.ip_address}" is currently dead.'

        connection_status_dns = self.InspectDNS.check_connection_dead()

        if connection_status_dns != ConnectionStatus.CONNECTION_DEAD: 
            self.insert_connection_status_to_queue(log_info = log_info, level = ConnectionLevel.USER_VM, source_ip = self.user_ip_address, destination_ip = self.ip_address)
       
            return
            
        log_info = f'Connection User-DNS {self.InspectDNS.ip_address} is currently dead.'
        
        connection_status_isp = self.InspectISP.check_connection_dead()

        if connection_status_isp != ConnectionStatus.CONNECTION_DEAD: 
            self.insert_connection_status_to_queue(log_info = log_info, level = ConnectionLevel.USER_DNS, source_ip = self.user_ip_address, destination_ip = self.dns_ip_address)

            return
        
        log_info = f'Connection User-ISP {self.InspectISP.ip_address} is currently dead.'
        connection_status_router = self.InspectRouter.check_connection_dead()

        if connection_status_router != ConnectionStatus.CONNECTION_DEAD: 
            self.insert_connection_status_to_queue(log_info = log_info, level = ConnectionLevel.USER_ISP, source_ip = self.user_ip_address, destination_ip = self.isp_ip_address)

            return


        log_info = f'Connection User-Router {self.InspectRouter.ip_address} is currently dead.'
        self.insert_connection_status_to_queue(log_info = log_info, level = ConnectionLevel.USER_ROUTER, source_ip = self.user_ip_address, destination_ip = self.router_ip_address)
        


    #  """
    # Handles the ping operation, checks the connection status, and logs the results.
    # Also sends metrics if monitoring API is enabled.

    # Args:
    #     log_name (str, optional): The name of the log. Defaults to ''.
    #     metric_name (str, optional): The name of the metric. Defaults to ''.
    # """

    def ping_handler(self, log_name = '', metric_name = ''):
        ping_gc_data = self.InspectGC.insert_connection_data()
        ping_dns_data = self.InspectDNS.insert_connection_data()
        ping_router_data = self.InspectRouter.insert_connection_data()
        ping_isp_data = self.InspectISP.insert_connection_data()

        print_ping_data(ping_gc_data)

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
                if self.enable_logging_api: self.logging(ping_gc_data, log_name)
            
        


