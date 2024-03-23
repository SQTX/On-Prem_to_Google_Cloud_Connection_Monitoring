import json

def load_instances():
    INSTANCES_PATH = './Data/instances.json'
    with open(INSTANCES_PATH, 'r') as file:
        data = json.load(file)

    return data