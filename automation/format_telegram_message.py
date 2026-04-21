import json

def format_message(file_path="shutdown_report.json"):
    try:
        with open(file_path, "r") as f:
            report = json.load(f)

        lines = []
        lines.append("Azure VM Automation Report\n")

        for vm in report.get("vms", []):
            lines.append(f"VM: {vm['vm_name']}")
            lines.append(f"Status: {vm['status']}")
            lines.append(f"Avg CPU: {vm['average_cpu_percent']}")
            lines.append(f"Samples: {vm['sample_count']}")
            lines.append(f"Decision: {vm['decision']}")
            lines.append(f"Dry Run: {vm['dry_run']}")
            lines.append("")

        return "\n".join(lines)

    except Exception as e:
        return f"Error generating report: {str(e)}"


if __name__ == "__main__":
    print(format_message())
