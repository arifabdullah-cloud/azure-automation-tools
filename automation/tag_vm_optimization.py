from datetime import datetime, timedelta

from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.monitor.query import MetricsQueryClient

SUBSCRIPTION_ID = "23ff688d-01fd-4a9f-b865-14fd60150c77"
DRY_RUN = False


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


def build_tags(existing_tags, status):
    tags = dict(existing_tags or {})
    tags["optimizationStatus"] = status.lower()
    tags["lastAnalyzedUtc"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    return tags


def apply_tags_to_vm(vm, status):
    compute_client = get_compute_client()

    resource_group = vm.id.split("/")[4]
    vm_name = vm.name
    updated_tags = build_tags(vm.tags, status)

    if DRY_RUN:
        print(f"[DRY RUN] Would tag VM '{vm_name}' in resource group '{resource_group}'")
        print(f"          optimizationStatus={status.lower()}")
        print(f"          tags={updated_tags}\n")
        return

    update_parameters = {"tags": updated_tags}

    compute_client.virtual_machines.begin_update(
        resource_group_name=resource_group,
        vm_name=vm_name,
        parameters=update_parameters,
    ).result()

    print(f"[UPDATED] Tagged VM '{vm_name}' with optimizationStatus={status.lower()}\n")


def main():
    vms = list_vms()

    if not vms:
        print("No VMs found in this subscription.")
        return

    print(f"Found {len(vms)} VM(s).\n")

    for vm in vms:
        print(f"Analyzing VM: {vm.name}")

        cpu_values = get_cpu_usage(vm.id)
        avg_cpu = calculate_average(cpu_values)
        sample_count = len(cpu_values)
        status = classify_vm(avg_cpu, sample_count)

        print(f"  Samples: {sample_count}")
        print(f"  Avg CPU: {round(avg_cpu, 2) if avg_cpu is not None else 'NO DATA'}")
        print(f"  Status: {status}")

        apply_tags_to_vm(vm, status)


if __name__ == "__main__":
    main()
