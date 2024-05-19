from Utlis.init_google_cloud import set_gcloud_project

from Utlis.config_handler import ConfDataType, get_config_data, yaml_2_json
from Probe.probing import Probing



    # """
    # Main execution block for the probing script. Sets up the Google Cloud project,
    # retrieves configuration data, initializes the Probing instance, and continuously
    # handles ping operations and logs the results.

    # This block:
    # 1. Sets the Google Cloud project.
    # 2. Retrieves VM configuration data and converts it to JSON format.
    # 3. Initializes the Probing instance with the configuration data.
    # 4. Enters an infinite loop to handle ping operations, logging, and monitoring.

    # The infinite loop:
    # 1. Retrieves log name and monitoring name from the configuration data.
    # 2. Calls the ping_handler method of the Probing instance with the log name and monitoring name.
    # """

if __name__ == '__main__':
    set_gcloud_project()

    config_data = get_config_data(ConfDataType.VMDATA)
    Probe = Probing(yaml_2_json(config_data))

    while True:
        log_name = get_config_data(ConfDataType.LOGINFO)['log-name']
        monitoring_name = get_config_data(ConfDataType.LOGINFO)['monitoring-name']

        Probe.ping_handler(log_name, monitoring_name)
