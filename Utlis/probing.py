import requests
from icmplib import ping

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