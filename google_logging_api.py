
from google.cloud import logging

import os

os.environ["GCLOUD_PROJECT"] = "przemeksroka-joonix-log-test"

PING_LOG_NAME = 'my-log'
CURL_LOG_NAME = 'curl-log'


def logging_api(data, log_name):
    logging_client = logging.Client()

    logger = logging_client.logger(log_name)
    
    logger.log_struct(data)

    print("Logged: {}".format(data))  

