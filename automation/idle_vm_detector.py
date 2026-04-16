from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient

SUBSCRIPTION_ID = "23ff688d-01fd-4a9f-b865-14fd60150c77"


def get_compute_client():
    credential = DefaultAzureCredential()
    return ComputeManagementClient(credential, SUBSCRIPTION_ID)


def list_vms(compute_client):
    return list(compute_client.virtual_machines.list_all())


def print_vm_info(vms):
    if not vms:
        print("No VMs found.")
        return

    for vm in vms:
        print(f"Name: {vm.name}")
        print(f"Location: {vm.location}")
        print("-" * 40)


def main():
    print("Fetching VMs...\n")
    compute_client = get_compute_client()
    vms = list_vms(compute_client)
    print_vm_info(vms)


if __name__ == "__main__":
    main()
