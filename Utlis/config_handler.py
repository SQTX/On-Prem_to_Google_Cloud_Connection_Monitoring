import os
import json
import yaml

from pathlib import Path
from enum import Enum


# ** PRIVATE *********************************************************************************************************
__CONFIG_FILE_PATH = Path('./user-config.yaml')
__PATH_FOR_JSON_FILE = Path('./config.json')

'''
Function for reading configuration
Returns:
    dict: Configuration data read from the file
'''
def __read_config():
    with open(__CONFIG_FILE_PATH, 'r') as stream:
        return yaml.safe_load(stream)


# ** PUBLIC **********************************************************************************************************
'''
Configuration sections
'''
class ConfDataType(Enum):
    MAIN = 1
    VMDATA = 2
    LOGINFO = 3
    ADDRESS = 4
    ADMINDATA = 5


'''
# Function returning data from the configuration file
Arg:
    config_type (ConfDataType): Selected configuration section
Return:
    dict: Configuration data
'''
def get_config_data(config_type):
    config = __read_config()

    if config_type.value == 1:
        return config['main']
    elif config_type.value == 2:
        return config['vm-data']
    elif config_type.value == 3:
        return config['log-info']
    elif config_type.value == 4:
        return config['addresses']
    elif config_type.value == 5:
        return config['project-admin-data']
    else:
        return -1


'''
Function converting YAML to JSON
Args:
    config_yaml (dict): YAML configuration data to be converted
Returns:
    dict: Converted JSON configuration data
'''
def yaml_2_json(config_yaml):
    with open(__PATH_FOR_JSON_FILE, 'w') as json_file:
        json.dump(config_yaml, json_file)

    # config_json = json.dumps(json.load(open('config.json')), indent=2)
    config_json = json.load(open(__PATH_FOR_JSON_FILE))

    if os.path.exists(__PATH_FOR_JSON_FILE):
        os.remove(__PATH_FOR_JSON_FILE)

    return config_json
