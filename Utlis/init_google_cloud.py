import os
from Utlis.config_handler import get_config_data, ConfDataType


__PROJECT_ID = get_config_data(ConfDataType.MAIN)['project-id']
__ENVIRONMENT = get_config_data(ConfDataType.MAIN)['environment']
# __ENVIRONMENT = 'GCLOUD_PROJECT'  # Default value


def set_gcloud_project():
    os.environ[__ENVIRONMENT] = __PROJECT_ID
