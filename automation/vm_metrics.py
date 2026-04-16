from datetime import datetime, timedelta
from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsQueryClient


SUBSCRIPTION_ID = "23ff688d-01fd-4a9f-b865-14fd60150c77"


def get_metrics_client():
    credential = DefaultAzureCredential()
    return MetricsQueryClient(credential)


def calculate_average(cpu_values):
    valid = [v for v in cpu_values if v is not None]
    return sum(valid) / len(valid) if valid else 0


def get_cpu_usage(resource_id):
    client = get_metrics_client()

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=30)

    response = client.query_resource(
        resource_id,
        metric_names=["Percentage CPU"],
        timespan=(start_time, end_time),
    )

    cpu_values = []

    print("\n--- CPU METRICS ---")

    for metric in response.metrics:
        for time_series in metric.timeseries:
            for data in time_series.data:

                cpu = data.average

                print(f"Timestamp: {data.timestamp}, CPU: {cpu}")

                # collect only valid values
                if cpu is not None:
                    cpu_values.append(cpu)

    # -------------------------
    # INTELLIGENCE LAYER
    # -------------------------

    avg_cpu = calculate_average(cpu_values)

    print("\n--- SUMMARY ---")
    print(f"Average CPU: {avg_cpu:.2f}%")

    # Idle logic
    if avg_cpu < 5:
        print("Status: IDLE VM ⚠️ (candidate for shutdown)")
    elif avg_cpu < 20:
        print("Status: LOW USAGE 🟡")
    else:
        print("Status: ACTIVE VM ✅")


if __name__ == "__main__":
    resource_id = "/subscriptions/23ff688d-01fd-4a9f-b865-14fd60150c77/resourceGroups/test-vm-automation_group/providers/Microsoft.Compute/virtualMachines/test-vm-automation"
    get_cpu_usage(resource_id)
