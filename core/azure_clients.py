from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.monitor.query import MetricsQueryClient

from core.config import AZURE_SUBSCRIPTION_ID


def get_credential():
    return DefaultAzureCredential()


def get_compute_client():
    return ComputeManagementClient(get_credential(), AZURE_SUBSCRIPTION_ID)


def get_metrics_client():
    return MetricsQueryClient(get_credential())
