from core.azure_clients import get_compute_client
from core.metrics import get_cpu_usage, calculate_average, classify_vm
from core.tagging import apply_tags_to_vm

DRY_RUN = False


def list_vms():
    compute_client = get_compute_client()
    return list(compute_client.virtual_machines.list_all())


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

        apply_tags_to_vm(vm, status, dry_run=DRY_RUN)


if __name__ == "__main__":
    main()
