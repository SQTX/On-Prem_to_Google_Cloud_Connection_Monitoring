from google.cloud import monitoring_v3
import time

from Data.settings import PROJECT_ID
class Monitoring:
   
    def __init__(self, instance) -> None:
        self.monitoring_client = monitoring_v3.MetricServiceClient()
        self.instance = instance
    
        self.current_metric_setups = []

   
    def setup_metric(self, metric_type_name, metric_store_id):
        series = monitoring_v3.TimeSeries()
        series.metric.type = f"custom.googleapis.com/{metric_type_name}"
        series.metric.labels["store_id"] = {metric_store_id}
    
        series.resource.type = self.instance['resource']['type']
        series.resource.labels["instance_id"] = self.instance['resource']['instance_id']
        series.resource.labels["zone"] = self.instance['resource']['zone']

        self.current_metric_setups.append({metric_type_name : series})

        return series
        
    
    def create_timestamp():
        now = time.time()
        seconds = int(now)
        nanos = int((now - seconds) * 10**9)
        interval = monitoring_v3.TimeInterval(
            {"end_time": {"seconds": seconds, "nanos": nanos}}
        )

        return interval
    
    def add_point_to_series(self, value, series):
        interval = self.create_timestamp()

        point = monitoring_v3.Point({"interval": interval, "value": {"double_value": value}})
        series.points = [point]

        return series

    def write_time_series(self, value, metric_type_name, metric_store_id):
        series = self.current_metric_setups.get(metric_type_name) if self.current_metric_setups.get(metric_type_name) != None else self.setup_metric(metric_type_name, metric_store_id)
        series = self.add_point_to_series(value, series)

        self.create_time_series(request={"name": f'projects/{PROJECT_ID}', "time_series": [series]})