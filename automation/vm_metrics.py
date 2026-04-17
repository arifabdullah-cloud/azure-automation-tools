from datetime import datetime, timedelta
import json

from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsQueryClient

SUBSCRIPTION_ID = "23ff688d-01fd-4a9f-b865-14fd60150c77"

RESOURCE_ID = "/subscriptions/23ff688d-01fd-4a9f-b865-14fd60150c77/resourceGroups/test-vm-automation_group/providers/Microsoft.Compute/virtualMachines/test-vm-automation"
VM_NAME = "test-vm-automation"


def get_metrics_client():
    credential = DefaultAzureCredential()
    return MetricsQueryClient(credential)


def calculate_average(cpu_values):
    valid = [v for v in cpu_values if v is not None]
    return sum(valid) / len(valid) if valid else 0


def classify_vm(avg_cpu):
    if avg_cpu < 5:
        return "IDLE"
    if avg_cpu < 20:
        return "LOW_USAGE"
    return "ACTIVE"


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
                if cpu is not None:
                    cpu_values.append(cpu)

    return cpu_values


def save_report(vm_name, resource_id, avg_cpu, status):
    report = {
        "generated_at_utc": datetime.utcnow().isoformat(),
        "vm_name": vm_name,
        "resource_id": resource_id,
        "average_cpu_percent": round(avg_cpu, 2),
        "status": status,
        "recommendation": (
            "Candidate for shutdown or scheduling"
            if status == "IDLE"
            else "Keep under observation"
            if status == "LOW_USAGE"
            else "No action needed"
        ),
    }

    with open("single_vm_report.json", "w") as f:
        json.dump(report, f, indent=4)

    print("\nReport saved to single_vm_report.json")


def main():
    cpu_values = get_cpu_usage(RESOURCE_ID)
    avg_cpu = calculate_average(cpu_values)
    status = classify_vm(avg_cpu)

    print("\n--- SUMMARY ---")
    print(f"VM Name: {VM_NAME}")
    print(f"Average CPU: {avg_cpu:.2f}%")
    print(f"Status: {status}")

    save_report(VM_NAME, RESOURCE_ID, avg_cpu, status)


if __name__ == "__main__":
    main()
