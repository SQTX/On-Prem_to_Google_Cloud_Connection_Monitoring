from enum import Enum


class ConnectionLevel(Enum):
    USER_VM = 1
    USER_DNS = 2
    USER_ROUTER = 3
    USER_ISP = 4
    USER_CONNECTION_FINE_AGAIN = 5



    def __int__(self): return self.value

class ConnectionStatus(Enum):
    CONNECTION_DEAD = 1
    CANNOT_ESTABLISH_CONNECTION_DETAILS = 2

    CONNECTION_CURRENTLY_UNSTABLE = 3
    CONNECTION_CURRENTLY_FINE = 4

    CONNECTION_LONG_UNSTABLE = 5
    CONNECTION_LONG_FINE = 6

    CURRENTLY_CROSSED_RTT_RISK_LINE = 7
    CURRENTLY_CROSSED_RTT_DANGER_LINE = 8

    CURRENTLY_CROSSED_PACKET_LOSS_RISK_LINE = 9
    CURRENTLY_CROSSED_PACKET_LOSS_DANGER_LINE = 10

    CURRENTLY_CROSSED_RTT_AND_PACKET_LOSS_RISK_LINE = 11
    CURRENTLY_CROSSED_RTT_AND_PACKET_LOSS_DANGER_LINE = 12

    OVERALL_CONNECTION_IS_BEING_UNSTABLE_RTT = 13
    OVERALL_CONNECTION_IS_BEING_UNSTABLE_PACKET_LOSS = 14
    OVERALL_CONNECTION_IS_BEING_UNSTABLE = 15

    OVERALL_CONNECTION_IS_BEING_AWFUL_RTT = 16
    OVERALL_CONNECTION_IS_BEING_AWFUL_PACKET_LOSS = 17
    OVERALL_CONNECTION_IS_BEING_AWFUL = 18





def establish_log_message(connection_status, connection_level, packet_loss, rtt, source_ip, destination_ip):
    connection_level_message = {

        ConnectionLevel.USER_DNS : f'User({source_ip}) - DNS({destination_ip})',
        ConnectionLevel.USER_ROUTER : f'User({source_ip}) - Router({destination_ip})',
        ConnectionLevel.USER_VM : f'User({source_ip}) - VM({destination_ip})',
        ConnectionLevel.USER_ISP : f'User({source_ip}) - ISP({destination_ip})'

    }

    create_log_structure = lambda message, level, s_ip, d_ip, pl, r: {

            'log_message' : message,
            'connection_level' : level,
            'source_ip' : s_ip,
            'destination_ip' : d_ip,
            'rtt' : r,
            'packet_loss' : pl
        
    }

    connection_status_message = {

    ConnectionStatus.CONNECTION_DEAD : create_log_structure(f'Connection {connection_level_message[connection_level]} failed.', connection_level, source_ip, destination_ip, packet_loss, rtt),
   
    ConnectionStatus.CONNECTION_CURRENTLY_FINE :  create_log_structure(f'Connection {connection_level_message[connection_level]} is working fine again.', connection_level, source_ip, destination_ip, packet_loss, rtt),
   

    ConnectionStatus.CURRENTLY_CROSSED_RTT_RISK_LINE :  create_log_structure(f'Connection {connection_level_message[connection_level]} crossed RTT-RISK-LINE.', connection_level, source_ip, destination_ip, packet_loss, rtt),
   
    ConnectionStatus.CURRENTLY_CROSSED_RTT_DANGER_LINE :  create_log_structure(f'Connection {connection_level_message[connection_level]} crossed RTT-DANGER-LINE', connection_level, source_ip, destination_ip, packet_loss, rtt),
   

    ConnectionStatus.CURRENTLY_CROSSED_PACKET_LOSS_RISK_LINE :  create_log_structure(f'Connection {connection_level_message[connection_level]} crossed PACKET-LOSS-RISK-LINE.', connection_level, source_ip, destination_ip, packet_loss, rtt),
   
    ConnectionStatus.CURRENTLY_CROSSED_PACKET_LOSS_DANGER_LINE :  create_log_structure(f'Connection {connection_level_message[connection_level]} crossed PACKET-LOSS-DANGER-LINE.', connection_level, source_ip, destination_ip, packet_loss, rtt),
   

    ConnectionStatus.CURRENTLY_CROSSED_RTT_AND_PACKET_LOSS_RISK_LINE :  create_log_structure(f'Connection {connection_level_message[connection_level]} crossed both RTT and PACKET-LOSS RISK-LINE.', connection_level, source_ip, destination_ip, packet_loss, rtt),
   
    ConnectionStatus.CURRENTLY_CROSSED_RTT_AND_PACKET_LOSS_DANGER_LINE :  create_log_structure(f'Connection {connection_level_message[connection_level]} crossed both RTT and PACKET-LOSS DANGER-LINE.', connection_level, source_ip, destination_ip, packet_loss, rtt),
   

    ConnectionStatus.OVERALL_CONNECTION_IS_BEING_UNSTABLE_RTT :  create_log_structure(f'Connection {connection_level_message[connection_level]} is being unstable due to the RTT rise.', connection_level, source_ip, destination_ip, packet_loss, rtt),
   
    ConnectionStatus.OVERALL_CONNECTION_IS_BEING_UNSTABLE_PACKET_LOSS :  create_log_structure(f'Connection {connection_level_message[connection_level]} is being unstable due to the PACKET-LOSS rise.', connection_level, source_ip, destination_ip, packet_loss, rtt),
   
    ConnectionStatus.OVERALL_CONNECTION_IS_BEING_UNSTABLE : reate_log_structure(f'Connection {connection_level_message[connection_level]} is being unstable due to the PACKET-LOSS rise.', connection_level, source_ip, destination_ip, packet_loss, rtt),

    ConnectionStatus.OVERALL_CONNECTION_IS_BEING_AWFUL_RTT : '',
    ConnectionStatus.OVERALL_CONNECTION_IS_BEING_AWFUL_PACKET_LOSS : '',
    ConnectionStatus.OVERALL_CONNECTION_IS_BEING_AWFUL : '',


}
    

    






