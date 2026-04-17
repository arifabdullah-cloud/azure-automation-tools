from datetime import datetime

from core.azure_clients import get_compute_client


def build_tags(existing_tags, status):
    tags = dict(existing_tags or {})
    tags["optimizationStatus"] = status.lower()
    tags["lastAnalyzedUtc"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    return tags


def apply_tags_to_vm(vm, status, dry_run=True):
    compute_client = get_compute_client()

    resource_group = vm.id.split("/")[4]
    vm_name = vm.name
    updated_tags = build_tags(vm.tags, status)

    if dry_run:
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
