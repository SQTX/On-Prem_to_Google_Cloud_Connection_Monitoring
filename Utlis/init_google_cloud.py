import os

PROJECT_ID = 'przemeksroka-joonix-log-test'
ENVIRONMENT = 'GCLOUD_PROJECT'

def set_gcloud_project():
    os.environ[ENVIRONMENT] = PROJECT_ID