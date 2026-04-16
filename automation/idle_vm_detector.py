from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient

# Azure Subscription ID
SUBSCRIPTION_ID = "23ff688d-01fd-4a9f-b865-14fd60150c77"


def list_vms():
    credential = DefaultAzureCredential()
    compute_client = ComputeManagementClient(credential, SUBSCRIPTION_ID)

    print("Fetching VMs...\n")

    for vm in compute_client.virtual_machines.list_all():
        print(f"Name: {vm.name}")
        print(f"Location: {vm.location}")
        print(f"Resource ID: {vm.id}")
        print("-" * 40)


if __name__ == "__main__":
    list_vms()
