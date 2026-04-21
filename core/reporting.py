import json
from datetime import datetime


def save_shutdown_report(results, filename="shutdown_report.json"):
    report = {
        "generated_at_utc": datetime.utcnow().isoformat(),
        "vm_count": len(results),
        "vms": results,
    }

    with open(filename, "w") as f:
        json.dump(report, f, indent=4)

    print(f"\nReport saved to {filename}")
