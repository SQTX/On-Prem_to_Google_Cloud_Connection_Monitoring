from Utlis.init_google_cloud import set_gcloud_project

from Utlis.config_handler import get_config_data, yaml_2_json, ConfDataType
from Probe.probing import Probing


if __name__ == '__main__':
    set_gcloud_project()

    config_data = get_config_data(ConfDataType.VMDATA)
    Probe = Probing(yaml_2_json(config_data))
    

    while True:
        log_name = get_config_data(ConfDataType.LOGINFO)['log-name']
        monitoring_name = get_config_data(ConfDataType.LOGINFO)['monitoring-name']

        Probe.ping_handler(log_name, monitoring_name)
