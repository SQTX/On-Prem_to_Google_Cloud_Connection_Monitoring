from google.cloud import logging


#  """
#     A class used to handle logging operations.

#     Attributes:
#         logging_client (logging.Client): The logging client instance.
#     """
class Logging:
    

    #    """
    #     Initializes the Logging class by creating a logging client instance.
    #     """
    def __init__(self):
        self.logging_client = logging.Client()



        # """
        # Sends log data to the specified logger.

        # Args:
        #     data (dict): The data to be logged.
        #     log_name (str): The name of the log.
        # """
    def send_logs(self, data, log_name):

        logger = self.logging_client.logger(log_name)

        try: logger.log_struct(data)

        except: print('[INFO] Cannot write log structure.')

