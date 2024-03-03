
import re 
import subprocess
import os

def ping_parser(ping_response):
    ip_match = re.search(r'([0-9]{1,3}\.){3}[0-9]{1,3}', ping_response)
    min_avg_max_stddev_match = re.search(r'[0-9]+\.[0-9]+/[0-9]+\.[0-9]+/[0-9]+\.[0-9]+/([0-9]+\.[0-9]+|nan)', ping_response)
    ttl_match = re.search(r'ttl=\d+', ping_response)
    time_match = re.search(r'time=[0-9]+\.[0-9]+', ping_response)
    packet_loss_match = re.search(r'[0-9]+\.[0-9]+% packet loss', ping_response)
    
    try:
        ip = str(ip_match.group(0))
        min, avg, max, stddev = str(min_avg_max_stddev_match.group(0)).split('/')
        ttl = int(str(ttl_match.group(0)).split('=')[1])
        time = float(str(time_match.group(0)).split('=')[1])
        packet_loss = float(str(packet_loss_match.group(0)).split(' ')[0][:-1]) / 100

    except:
        print("Packet loss 100%")

    ping_stats = {

        'ip' : ip,
        'min' : float(min),
        'avg' : float(avg),
        'max' : float(max),
        'stdev' : float(stddev),
        'ttl' : ttl,
        'time' : time,
        'packet-loss' : packet_loss

    }

    return ping_stats


def send_ping():
    server_address = "34.118.37.108"

    try:
        ping_response = os.popen(f"ping {server_address} -c 1").read()
        ping_stats = ping_parser(ping_response)

    except subprocess.CalledProcessError:
        print("Failed to send ping.")

    return ping_stats