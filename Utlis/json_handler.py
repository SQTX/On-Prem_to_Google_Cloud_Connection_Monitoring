import json

def load_instances():
    INSTANCES_PATH = './Data/instances.json'
    with open(INSTANCES_PATH, 'r') as f:
        data = json.load(f)

    return data