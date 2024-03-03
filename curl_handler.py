import requests

def send_curl():
    server_address = "34.118.37.108"

    try:
        response = requests.get('http://' + server_address)

        curl_log = {

            'status-code' : response.status_code,
            'status-response' : response.reason,
            'delta-time' : response.elapsed.total_seconds()

        }
       
    except requests.RequestException as e:
        print(f"Failed to send HTTP request: {e}")

    return curl_log