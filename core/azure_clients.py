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
