import time

from curl_handler import send_curl
from ping_handler import send_ping

from google_logging_api import logging_api
from google_logging_api import PING_LOG_NAME, CURL_LOG_NAME

try:
    run = True
    while run:
        ping_stats = send_ping()
        logging_api(ping_stats, PING_LOG_NAME)

        curl_log = send_curl()
        logging_api(curl_log, CURL_LOG_NAME)

        time.sleep(1)

except KeyboardInterrupt:
        print("Script terminated by user.")