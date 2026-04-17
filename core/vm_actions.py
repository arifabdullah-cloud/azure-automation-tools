from core.azure_clients import get_compute_client


def stop_vm(vm, dry_run=True):
    compute_client = get_compute_client()

    resource_group = vm.id.split("/")[4]
    vm_name = vm.name

    if dry_run:
        print(f"[DRY RUN] Would stop VM '{vm_name}' in resource group '{resource_group}'\n")
        return

    compute_client.virtual_machines.begin_deallocate(
        resource_group_name=resource_group,
        vm_name=vm_name,
    ).result()

    print(f"[UPDATED] Stopped VM '{vm_name}'\n")
