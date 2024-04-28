import numpy

from .connection_status import ConnectionStatus
from Utlis.probing import ping_ip

class Supervisor():

    RTT_RISK_LINE = 150
    PACKET_LOSS_RISK_LINE = 5

    RTT_DANGER_LINE = 300
    PACKET_LOSS_DANGER_LINE = 15

    RTT_DEAD_LINE = 600
    PACKET_LOSS_DEAD_LINE = 0.5

    MAX_CURRENT_LENGTH = 3
    MAX_LONG_LENGTH = 15

    def __init__(self, ip_address):
        self.ip_address = ip_address

        self.rtt_current = []
        self.packet_loss_current = []
        self.jitter_current = []

        self.rtt_long = []
        self.packet_loss_long = []
        self.jitter_long =  []
    

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


    def check_connection_dead(self):
        if len(self.rtt_current) < 2:
            return ConnectionStatus.CANNOT_ESTABLISH_CONNECTION_DETAILS
        
        avg_packet_loss = numpy.average(self.packet_loss_current)
        avg_rtt = numpy.average(self.rtt_current)
        print(avg_packet_loss)

        if avg_packet_loss >= self.PACKET_LOSS_DEAD_LINE or (avg_packet_loss == 0 and avg_rtt == 0):
            return ConnectionStatus.CONNECTION_DEAD
        
        if avg_packet_loss == 0:
            return ConnectionStatus.CONNECTION_CURRENTLY_FINE
    
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