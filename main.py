from Utlis.json_handler import load_instances
from Utlis.init_google_cloud import set_gcloud_project

from Probe.probing import Probing

import time

if __name__ == '__main__':
    set_gcloud_project()
    instance = load_instances()

    Probe = Probing(instance)

    while True:
        data = Probe.ping_instance()

        Probe.logging(data, 'ping-instance-logs')
        Probe.monitoring(data['jitter'], 'ping-instance-monitoring', 'Pittsburgh')

        time.sleep(10)
    

    
