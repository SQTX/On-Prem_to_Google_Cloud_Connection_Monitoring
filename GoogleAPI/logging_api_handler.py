from google.cloud import logging
class Logging:
    
    def __init__(self) -> None:
        self.logging_client = logging.Client()

    def send_logs(self, data, log_name):

        logger = self.logging_client.logger(log_name)
        
        logger.log_struct(data)

