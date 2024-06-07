from google.cloud import monitoring_v3
import time
from Utlis.config_handler import ConfDataType, get_config_data


PROJECT_ID = get_config_data(ConfDataType.MAIN)['project-id']


# """
#     A class used to handle monitoring operations with Google Cloud Monitoring.

#     Attributes:
#         monitoring_client (monitoring_v3.MetricServiceClient): The monitoring client instance.
#         instance (dict): The instance-specific information.
#         current_metric_setups (list): A list to store the current metric setups.
#     """
class Monitoring:
   

    #     """
    # Initializes the Monitoring class by creating a monitoring client instance
    # and setting up the instance-specific information.

    # Args:
    #     instance (dict): A dictionary containing instance-specific information.
    # """

    def __init__(self, instance) -> None:
        self.monitoring_client = monitoring_v3.MetricServiceClient()
        self.instance = instance

        self.current_metric_setups = []

   
    # """
    # Sets up a metric series for a given metric type name.

    # Args:
    #     metric_type_name (str): The name of the metric type.

    # Returns:
    #     monitoring_v3.TimeSeries: The time series object for the metric.
    # """
    def setup_metric(self, metric_type_name):
        series = monitoring_v3.TimeSeries()
        series.metric.type = f"custom.googleapis.com/{metric_type_name}"
        series.metric.labels["store_id"] = 'Pittsburgh'
    
        series.resource.type = self.instance['resource']['type']
        series.resource.labels["instance_id"] = self.instance['resource']['labels']['instance_id']
        series.resource.labels["zone"] = self.instance['resource']['labels']['zone']

        self.current_metric_setups.append({metric_type_name : series})

        return series
        

    #     """
    # Creates a timestamp for the current time.

    # Returns:
    #     monitoring_v3.TimeInterval: The time interval object with the current time.
    # """ 
    def create_timestamp(self):

        now = int(time.time())
        seconds = int(now)
        nanos = int((now - seconds) * 10**9)
        interval = monitoring_v3.TimeInterval(
            {"end_time": {"seconds": seconds, "nanos": nanos}}
        )

        return interval
    

    #     """
    # Adds a data point to the given time series.

    # Args:
    #     value (float): The value of the data point.
    #     series (monitoring_v3.TimeSeries): The time series to add the data point to.

    # Returns:
    #     monitoring_v3.TimeSeries: The updated time series object.
    # """
    def add_point_to_series(self, value, series):
        interval = self.create_timestamp()
    
        point = monitoring_v3.Point({"interval": interval, "value": {"double_value": value}})
        series.points = [point]

        return series


    #     """
    # Writes a time series data point to the monitoring client.

    # Args:
    #     value (float): The value of the data point.
    #     metric_type_name (str): The name of the metric type.

    # Returns:
    #     bool: True if the time series data was successfully written, False otherwise.
    # """
    def write_time_series(self, value, metric_type_name):
        series = None
        for i in self.current_metric_setups:
            if i.get(metric_type_name) != None: 
                series = i[metric_type_name]
                break
            
        if series == None: series = self.setup_metric(metric_type_name)
        series = self.add_point_to_series(value, series)

        try:
            self.monitoring_client.create_time_series(request={"name": f'projects/{PROJECT_ID}', "time_series": [series]}, timeout = 2)
            return True

        except:
            print('[INFO] Cannot write metric')
            return False

       