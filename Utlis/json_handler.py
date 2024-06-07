import json
from pathlib import Path

def load_instances():
    INSTANCES_PATH = Path('./Data/instances.json')
    with open(INSTANCES_PATH, 'r') as f:
        data = json.load(f)

    return data