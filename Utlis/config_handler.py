import yaml

from pathlib import Path
from enum import Enum


__CONFIG_FILE_PATH = Path('./user-config.yaml')

def __read_config():
    with open(__CONFIG_FILE_PATH, 'r') as stream:
        return yaml.safe_load(stream)

class ConfDataType(Enum):
    MAIN = 1
    LOGINFO = 2
    ADDRESS = 3
    ADMINDATA = 4

def get_config_data(config_type):
    config = __read_config()

    if config_type.value == 1:
        return config['main']
    elif config_type.value == 2:
        return config['log-info']
    elif config_type.value == 3:
        return config['addresses']
    elif config_type.value == 4:
        return config['project-admin-data']
    else:
        return -1
