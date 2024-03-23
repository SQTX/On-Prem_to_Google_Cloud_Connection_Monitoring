import os

from Data.settings import PROJECT_ID

ENVIRONMENT = 'GCLOUD_PROJECT'

def set_gcloud_project():
    os.environ[ENVIRONMENT] = PROJECT_ID