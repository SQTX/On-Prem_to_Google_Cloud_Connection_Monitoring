import numpy

from .connection_status import ConnectionStatus
from Utlis.probing import ping_ip


    # """
    # A class used to supervise network connections by monitoring RTT, packet loss, and jitter.

    # Attributes:
    #     RTT_RISK_LINE (int): Threshold for RTT to be considered at risk.
    #     PACKET_LOSS_RISK_LINE (int): Threshold for packet loss to be considered at risk.
    #     RTT_DANGER_LINE (int): Threshold for RTT to be considered dangerous.
    #     PACKET_LOSS_DANGER_LINE (int): Threshold for packet loss to be considered dangerous.
    #     RTT_DEAD_LINE (int): Threshold for RTT to be considered dead.
    #     PACKET_LOSS_DEAD_LINE (float): Threshold for packet loss to be considered dead.
    #     MAX_CURRENT_LENGTH (int): Maximum length of the current data window.
    #     MAX_LONG_LENGTH (int): Maximum length of the long-term data window.
    #     ip_address (str): IP address to be monitored.
    #     rtt_current (list): List to store current RTT values.
    #     packet_loss_current (list): List to store current packet loss values.
    #     jitter_current (list): List to store current jitter values.
    #     rtt_long (list): List to store long-term RTT values.
    #     packet_loss_long (list): List to store long-term packet loss values.
    #     jitter_long (list): List to store long-term jitter values.
    # """
class Supervisor():

    RTT_RISK_LINE = 150
    PACKET_LOSS_RISK_LINE = 5

    RTT_DANGER_LINE = 300
    PACKET_LOSS_DANGER_LINE = 15

    RTT_DEAD_LINE = 600
    PACKET_LOSS_DEAD_LINE = 0.5

    MAX_CURRENT_LENGTH = 3
    MAX_LONG_LENGTH = 15



        #  """
        # Initializes the Supervisor class with the given IP address.

        # Args:
        #     ip_address (str): The IP address to be monitored.
        # """

    def __init__(self, ip_address):
        self.ip_address = ip_address

        self.rtt_current = []
        self.packet_loss_current = []
        self.jitter_current = []

        self.rtt_long = []
        self.packet_loss_long = []
        self.jitter_long =  []
    

    # """
    # Pings the IP address and inserts the collected data into the current and long-term data windows.

    # Returns:
    #     dict: A dictionary containing the ping data.
    # """
    def insert_connection_data(self):
        ping_data = ping_ip(self.ip_address)

        rtt = ping_data['avg_rtt']
        packet_loss = ping_data['packet_loss']
        jitter = ping_data['jitter']

        if len(self.rtt_current) == self.MAX_CURRENT_LENGTH:
            self.rtt_current.pop(0)
            self.packet_loss_current.pop(0)
            self.jitter_current.pop(0)

        if len(self.rtt_long) == self.MAX_LONG_LENGTH:
            self.rtt_long.pop(0)
            self.packet_loss_long.pop(0)
            self.jitter_long.pop(0)

        self.rtt_current.append(rtt)
        self.packet_loss_current.append(packet_loss)
        self.jitter_current.append(jitter)

        self.rtt_long.append(rtt)
        self.packet_loss_long.append(packet_loss)
        self.jitter_long.append(jitter)

        return ping_data



    #     """
    # Checks if the connection is dead based on the current RTT and packet loss data.

    # Returns:
    #     ConnectionStatus: The status of the connection.
    # """
    def check_connection_dead(self):
        if len(self.rtt_current) < 2:
            return ConnectionStatus.CANNOT_ESTABLISH_CONNECTION_DETAILS
        
        avg_packet_loss = numpy.average(self.packet_loss_current)
        avg_rtt = numpy.average(self.rtt_current)
        print(f'# Current average packet-loss: {avg_packet_loss}')

        if avg_packet_loss >= self.PACKET_LOSS_DEAD_LINE or (avg_packet_loss == 0 and avg_rtt == 0):
            return ConnectionStatus.CONNECTION_DEAD
        
        if avg_packet_loss == 0:
            return ConnectionStatus.CONNECTION_CURRENTLY_FINE
    


    #     """
    # Checks the stability of the connection based on current and long-term RTT and packet loss data.

    # Returns:
    #     tuple or ConnectionStatus: A tuple with the connection status, average packet loss, and average RTT
    #                                 if the stability can be evaluated, otherwise just the connection status.
    # """
    def check_connection_stability(self):
        can_eval_current_connection = False
        can_eval_long_connection = False
        
        if len(current_avg_rtt) == self.MAX_CURRENT_LENGTH:
            can_eval_current_connection = True
            current_avg_packet_loss = numpy.average(self.packet_loss_current)
            current_avg_rtt = numpy.average(self.rtt_current)
        
        if len(long_avg_rtt) == self.MAX_LONG_LENGTH:
            can_eval_long_connection = True
            long_avg_packet_loss = numpy.average(self.packet_loss_long[:(-1) * self.MAX_CURRENT_LENGTH])
            long_avg_rtt = numpy.average(self.rtt_long[:(-1) * self.MAX_CURRENT_LENGTH])


        if can_eval_current_connection == False:
            print('Currently cannot establish connection stability.')
         
        current_connection_status = None

        if can_eval_long_connection:
            return_connection_status = lambda x: (x, long_avg_packet_loss, long_avg_rtt)

            if long_avg_packet_loss >= self.PACKET_LOSS_DANGER_LINE and long_avg_rtt >= self.RTT_DANGER_LINE: 
                return return_connection_status(ConnectionStatus.OVERALL_CONNECTION_IS_BEING_AWFUL)

            if long_avg_packet_loss >= self.PACKET_LOSS_DANGER_LINE:
                return return_connection_status(ConnectionStatus.OVERALL_CONNECTION_IS_BEING_AWFUL_PACKET_LOSS)

            if long_avg_rtt >= self.RTT_DANGER_LINE:
                return return_connection_status(ConnectionStatus.OVERALL_CONNECTION_IS_BEING_AWFUL_RTT)


            if long_avg_packet_loss >= self.PACKET_LOSS_RISK_LINE and long_avg_rtt >= self.RTT_RISK_LINE: 
                return return_connection_status(ConnectionStatus.OVERALL_CONNECTION_IS_BEING_UNSTABLE)

            if long_avg_packet_loss >= self.PACKET_LOSS_RISK_LINE:
                return return_connection_status(ConnectionStatus.OVERALL_CONNECTION_IS_BEING_UNSTABLE_PACKET_LOSS)

            if long_avg_rtt >= self.RTT_RISK_LINE:
                return return_connection_status(ConnectionStatus.OVERALL_CONNECTION_IS_BEING_UNSTABLE_RTT)


        if can_eval_current_connection:
            return_connection_status = lambda x: (x, current_avg_packet_loss, current_avg_rtt)

            if current_avg_packet_loss >= self.PACKET_LOSS_DANGER_LINE and current_avg_rtt >= self.RTT_DANGER_LINE: 
                return return_connection_status(ConnectionStatus.CURRENTLY_CROSSED_RTT_AND_PACKET_LOSS_DANGER_LINE)

            if current_avg_packet_loss >= self.PACKET_LOSS_DANGER_LINE:
                return return_connection_status(ConnectionStatus.CURRENTLY_CROSSED_PACKET_LOSS_DANGER_LINE)

            if current_avg_rtt >= self.RTT_DANGER_LINE:
                return return_connection_status(ConnectionStatus.CURRENTLY_CROSSED_RTT_DANGER_LINE)


            if current_avg_packet_loss >= self.PACKET_LOSS_RISK_LINE and current_avg_rtt >= self.RTT_RISK_LINE: 
                return return_connection_status(ConnectionStatus.CURRENTLY_CROSSED_RTT_AND_PACKET_LOSS_RISK_LINE)

            if current_avg_packet_loss >= self.PACKET_LOSS_RISK_LINE:
                return return_connection_status(ConnectionStatus.CURRENTLY_CROSSED_PACKET_LOSS_RISK_LINE)

            if current_avg_rtt >= self.RTT_RISK_LINE:
                return return_connection_status(ConnectionStatus.CURRENTLY_CROSSED_RTT_RISK_LINE)

        return ConnectionStatus.CONNECTION_CURRENTLY_FINE

class SupervisingRouter(Supervisor):
    pass

class SupervisingDNS(Supervisor):
    pass

class SupervisingISP(Supervisor):
    pass

class SupervisingGC(Supervisor):
    pass