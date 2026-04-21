from core.azure_clients import get_compute_client
from core.config import (
    DRY_RUN,
    MIN_SAMPLE_COUNT,
    PROTECTION_TAG_NAME,
    PROTECTION_TAG_VALUE,
)
from core.metrics import get_cpu_usage, calculate_average, classify_vm
from core.reporting import save_shutdown_report
from core.vm_actions import stop_vm


def list_vms():
    compute_client = get_compute_client()
    return list(compute_client.virtual_machines.list_all())


def is_protected_vm(vm):
    tags = vm.tags or {}
    value = tags.get(PROTECTION_TAG_NAME, "").lower()
    return value == PROTECTION_TAG_VALUE


def is_shutdown_candidate(status, sample_count):
    return status == "IDLE" and sample_count >= MIN_SAMPLE_COUNT


def main():
    vms = list_vms()

    if not vms:
        print("No VMs found in this subscription.")
        return

    print(f"Found {len(vms)} VM(s).\n")

    results = []

    for vm in vms:
        print(f"Analyzing VM: {vm.name}")

        cpu_values = get_cpu_usage(vm.id)
        avg_cpu = calculate_average(cpu_values)
        sample_count = len(cpu_values)
        status = classify_vm(avg_cpu, sample_count)

        print(f"  Samples: {sample_count}")
        print(f"  Avg CPU: {round(avg_cpu, 2) if avg_cpu is not None else 'NO DATA'}")
        print(f"  Status: {status}")

        if is_protected_vm(vm):
            decision = f"SKIP (protected by tag {PROTECTION_TAG_NAME}={PROTECTION_TAG_VALUE})"
            print(f"  Decision: {decision}\n")
        elif is_shutdown_candidate(status, sample_count):
            decision = "SHUTDOWN CANDIDATE"
            print(f"  Decision: {decision}")
            stop_vm(vm, dry_run=DRY_RUN)
        else:
            decision = "NO ACTION"
            print(f"  Decision: {decision}\n")

        results.append(
            {
                "vm_name": vm.name,
                "resource_id": vm.id,
                "sample_count": sample_count,
                "average_cpu_percent": round(avg_cpu, 2) if avg_cpu is not None else None,
                "status": status,
                "decision": decision,
                "dry_run": DRY_RUN,
            }
        )

    save_shutdown_report(results)


if __name__ == "__main__":
    main()
