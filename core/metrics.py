from datetime import datetime, timedelta

from core.azure_clients import get_metrics_client


def get_cpu_usage(resource_id, minutes=30):
    metrics_client = get_metrics_client()

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=minutes)

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


def get_recommendation(status):
    if status == "NO_DATA":
        return "No recent CPU data available. VM may be stopped, newly started, or not yet emitting metrics."
    if status == "INSUFFICIENT_DATA":
        return "Not enough datapoints yet. Wait a few more minutes and rerun."
    if status == "IDLE":
        return "Candidate for shutdown or scheduling."
    if status == "LOW_USAGE":
        return "Keep under observation for rightsizing or scheduling."
    return "No action needed."
