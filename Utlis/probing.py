import requests
from icmplib import ping


#  """
#     Pings the given IP address and returns the ping statistics.

#     Args:
#         ip_address (str): The IP address to ping.

#     Returns:
#         dict: A dictionary containing the ping statistics:
#             - ip_address (str): The IP address that was pinged.
#             - min_rtt (float): The minimum round-trip time.
#             - max_rtt (float): The maximum round-trip time.
#             - avg_rtt (float): The average round-trip time.
#             - packet_loss (float): The packet loss percentage.
#             - jitter (float): The jitter value.
#             - is_alive (bool): Indicates if the IP address is alive.
#     """

def ping_ip(ip_address):
    ping_raw = ping(address = ip_address, interval = 0.5, count = 2, timeout=1)
    

    data = {'ip_address'    :         ping_raw.address,
            'min_rtt'       :         ping_raw.min_rtt,
            'max_rtt'       :         ping_raw.max_rtt,
            'avg_rtt'       :         ping_raw.avg_rtt,
            'packet_loss'   :         ping_raw.packet_loss,
            'jitter'        :         ping_raw.jitter,
            'is_alive'      :         ping_raw.is_alive}

    if data['avg_rtt'] == 0 and data['packet_loss'] == 0: data['packet_loss'] = 1

    return data

def print_ping_data(data):
    print('\n')
    print('#', '-' * 30, '#')
    for key, value in data.items():
        print(f'{key} : {value}')
        
    
    print('#', '-' * 30, '#')
    print('\n')
    

    # """
    # Sends an HTTP GET request to the given IP address and returns the response statistics.

    # Args:
    #     ip_address (str): The IP address to send the HTTP GET request to.

    # Returns:
    #     dict: A dictionary containing the response statistics:
    #         - status_code (int): The HTTP status code of the response.
    #         - status_response (str): The HTTP status message of the response.
    #         - delta_time (float): The time taken to receive the response in seconds.
    #         - response_length (int): The length of the response content.
    #         - response_headers (dict): The headers of the response.
    #         - status_response (bool): False if the request failed.
    # """
def send_curl(ip_address):

    try:
        response = requests.get('http://' + ip_address)

        curl_log = {

            'status_code' : response.status_code,
            'status_response' : response.reason,
            'delta_time' : response.elapsed.total_seconds(),
            'response_length': len(response.content),
            'response_headers': dict(response.headers) 


        }

    
    except requests.RequestException as e:
        curl_log = {

            'delta_time' : 0,
            'status_response' : False

        }

        print(f"Failed to send HTTP request: {e}")

    return curl_log