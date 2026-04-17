from datetime import datetime
import json

from core.azure_clients import get_compute_client
from core.metrics import (
    get_cpu_usage,
    calculate_average,
    classify_vm,
    get_recommendation,
)


def list_vms():
    compute_client = get_compute_client()
    return list(compute_client.virtual_machines.list_all())


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
