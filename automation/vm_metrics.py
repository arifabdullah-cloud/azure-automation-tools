from datetime import datetime, timedelta
from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsQueryClient


SUBSCRIPTION_ID = "23ff688d-01fd-4a9f-b865-14fd60150c77"


def get_metrics_client():
    credential = DefaultAzureCredential()
    return MetricsQueryClient(credential)


def get_cpu_usage(resource_id):
    client = get_metrics_client()

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=30)

    response = client.query_resource(
        resource_id,
        metric_names=["Percentage CPU"],
        timespan=(start_time, end_time),
    )

    for metric in response.metrics:
        for time_series in metric.timeseries:
            for data in time_series.data:
                print(f"Timestamp: {data.timestamp}, CPU: {data.average}")
                
if __name__ == "__main__":
    resource_id = "/subscriptions/23ff688d-01fd-4a9f-b865-14fd60150c77/resourceGroups/test-vm-automation_group/providers/Microsoft.Compute/virtualMachines/test-vm-automation"
    get_cpu_usage(resource_id)
