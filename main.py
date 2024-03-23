from Utlis.json_handler import load_instances
from Utlis.init_google_cloud import set_gcloud_project

from Probe.probing import Probing

if __name__ == '__main__':
    set_gcloud_project()
    instance = load_instances()

    Probe = Probing(instance)
    
