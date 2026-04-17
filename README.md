# Azure Automation Tools

Practical Azure automation tools for cloud monitoring, utilization analysis, and operational tagging.

This project focuses on building hands-on cloud engineering capabilities using Azure SDKs, Azure Monitor metrics, and Python-based automation.

---

## 🚀 Features

- Discover Azure virtual machines in a subscription
- Query CPU usage from Azure Monitor
- Classify VMs based on recent utilization:
  - `NO_DATA`
  - `INSUFFICIENT_DATA`
  - `IDLE`
  - `LOW_USAGE`
  - `ACTIVE`
- Generate JSON utilization reports
- Apply optimization tags to Azure VMs

---

## 💡 Current Use Case

This project identifies underutilized Azure VMs based on CPU metrics and tags them with:

- `optimizationStatus`
- `lastAnalyzedUtc`

This forms the foundation for:

- Cost optimization workflows
- Scheduled shutdown systems
- Rightsizing recommendations
- AI-driven cloud operations

---

## 🏗️ Architecture

```text
Azure Subscription
    ↓
VM Discovery (Azure Compute SDK)
    ↓
CPU Metrics Query (Azure Monitor)
    ↓
Utilization Analysis
    ↓
Status Classification
    ↓
JSON Report / Azure Tag Update
```

---

## 📁 Project Structure

```text
azure-automation-tools/
│
├── automation/
│   ├── all_vm_metrics.py          # Scan all VMs and generate report
│   └── tag_vm_optimization.py    # Analyze and tag VMs
│
├── core/
│   ├── azure_clients.py          # Azure SDK clients
│   ├── config.py                 # Environment configuration
│   ├── metrics.py                # CPU analysis logic
│   └── tagging.py                # Tagging logic
│
├── architecture/
├── monitoring/
├── cost-management/
├── infrastructure/
│
├── .env.example
├── requirements.txt
└── README.md
```

## ⚙️ Setup

1. Install dependencies
   ```bash
   python3 -m pip install -r requirements.txt
   ```
2. Create ```.env```
   Copy ```env.example``` and update with your values:
   ```bash
   AZURE_SUBSCRIPTION_ID=your-subscription-id-here
   DRY_RUN=false
   CPU_LOOKBACK_MINUTES=30
   ```
3. Authenticate to Azure
   ```bash
   az login
   ```
4. Run
   Generate utilization report
   ```bash
   python3 -m automation.all_vm_metrics
   ```
   Analyze and tag VMs
   ```bash
   python3 -m automation.tag_vm_optimization
   ```

## 📊 Example Output

```bash
Found 1 VM(s).

Analyzing VM: test-vm-automation
  Samples: 30
  Avg CPU: 0.46
  Status: IDLE

[UPDATED] Tagged VM 'test-vm-automation' with optimizationStatus=idle
```

## 📄 Example Report

```bash
{
  "generated_at_utc": "2026-04-17T09:53:47.620708",
  "vm_count": 1,
  "vms": [
    {
      "vm_name": "test-vm-automation",
      "average_cpu_percent": 0.46,
      "sample_count": 30,
      "status": "IDLE",
      "recommendation": "Candidate for shutdown or scheduling."
    }
  ]
}
```

## 🧠 Key Concepts Demonstrated

- Azure SDK integration
- Azure Monitor metrics querying
- Infrastructure utilization analysis
- FinOps-style cost optimization logic
- Safe automation with dry-run capability
- Modular Python project structure

## 🔮 Future Improvements

- Support additional metrics (memory, disk, network)
- Add scheduled execution (Azure Functions / GitHub Actions)
- Implement safe auto-shutdown workflows for idle VMs
- Add dashboards or visualization layers
- Integrate AI for anomaly detection and recommendations

## 🎯 Goal

To build production-style Azure automation tools while strengthening skills in:

- Cloud engineering
- DevOps practices
- Infrastructure automation
- AI-assisted operations
   
