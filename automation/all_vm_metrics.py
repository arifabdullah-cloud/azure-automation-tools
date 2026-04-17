from datetime import datetime, timedelta
import json

from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.monitor.query import MetricsQueryClient

SUBSCRIPTION_ID = "23ff688d-01fd-4a9f-b865-14fd60150c77"


def get_credential():
    return DefaultAzureCredential()


def get_compute_client():
    return ComputeManagementClient(get_credential(), SUBSCRIPTION_ID)


def get_metrics_client():
    return MetricsQueryClient(get_credential())


def list_vms():
    compute_client = get_compute_client()
    return list(compute_client.virtual_machines.list_all())


def get_cpu_usage(resource_id):
    metrics_client = get_metrics_client()

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=30)

    response = metrics_client.query_resource(
        resource_id,
        metric_names=["Percentage CPU"],
        timespan=(start_time, end_time),
    )

    cpu_values = []

    for metric in response.metrics:
        for time_series in metric.timeseries:
            for data in time_series.data:
                if data.average is not None:
                    cpu_values.append(data.average)

    return cpu_values


def calculate_average(cpu_values):
    if not cpu_values:
        return None
    return sum(cpu_values) / len(cpu_values)


def classify_vm(avg_cpu, sample_count):
    if sample_count == 0:
        return "NO_DATA"
    if sample_count < 5:
        return "INSUFFICIENT_DATA"
    if avg_cpu < 5:
        return "IDLE"
    if avg_cpu < 20:
        return "LOW_USAGE"
    return "ACTIVE"


def get_recommendation(status):
    if status == "NO_DATA":
        return "No recent CPU data available. VM may be stopped, newly started, or not yet emitting metrics."
    if status == "INSUFFICIENT_DATA":
        return "Not enough datapoints yet. Wait a few more minutes and rerun."
    if status == "IDLE":
        return "Candidate for shutdown or scheduling."
    if status == "LOW_USAGE":
        return "Keep under observation for rightsizing or scheduling."
    return "No action needed."


def analyze_vm(vm):
    cpu_values = get_cpu_usage(vm.id)
    avg_cpu = calculate_average(cpu_values)
    sample_count = len(cpu_values)
    status = classify_vm(avg_cpu, sample_count)

    return {
        "vm_name": vm.name,
        "resource_id": vm.id,
        "average_cpu_percent": round(avg_cpu, 2) if avg_cpu is not None else None,
        "sample_count": sample_count,
        "status": status,
        "recommendation": get_recommendation(status),
    }


def save_report(results):
    report = {
        "generated_at_utc": datetime.utcnow().isoformat(),
        "vm_count": len(results),
        "vms": results,
    }

    with open("all_vm_report.json", "w") as f:
        json.dump(report, f, indent=4)

    print("\nReport saved to all_vm_report.json")


def main():
    vms = list_vms()

    if not vms:
        print("No VMs found in this subscription.")
        return

    results = []

    print(f"Found {len(vms)} VM(s).\n")

    for vm in vms:
        print(f"Analyzing VM: {vm.name}")
        result = analyze_vm(vm)
        results.append(result)

        print(f"  Samples: {result['sample_count']}")
        print(f"  Avg CPU: {result['average_cpu_percent']}")
        print(f"  Status: {result['status']}\n")

    save_report(results)


if __name__ == "__main__":
    main()
