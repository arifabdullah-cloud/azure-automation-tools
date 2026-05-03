# Azure Automation Tools

End-to-end Azure automation system for VM utilization analysis, cost optimization, and safe operational control.

This project demonstrates real-world cloud engineering practices using:
- Azure SDK (Compute + Monitor)
- Python automation
- GitHub Actions (scheduled execution)
- Telegram notifications
- Safe automation design patterns

---

## 🚀 Features

### 🔍 Discovery & Monitoring

- Discover Azure Virtual Machines across a subscription
- Query CPU metrics from Azure Monitor
- Analyze utilization over a configurable time window

### 🧠 Decision Engine

- Classify VMs based on utilization:
  - `NO_DATA`
  - `INSUFFICIENT_DATA`
  - `IDLE`
  - `LOW_USAGE`
  - `ACTIVE`
- Configurable thresholds and lookback windows
- Sample validation for reliable decisions

### ⚙️ Automation & Actions

- Tag VMs with optimization metadata:
  - `optimizationStatus`
  - `lastAnalyzedUtc`
- Identify shutdown candidates safely
- Execute **real VM shutdowns** (with dry-run support)
- Protection override via tag:
  - `doNotShutdown=true`

### 📦 Reporting & Notification

- Generate structured JSON reports
- Upload reports as GitHub Actions artifacts
- Send automation results via Telegram

### ⏱️ Scheduling

- Fully automated execution using GitHub Actions
- Supports:
  - scheduled runs (cron)
  - manual trigger

---

## 💡 Use Case

This project identifies underutilized Azure VMs and enables:

- Automated cost optimization
- Safe VM shutdown workflows
- Operational visibility via notifications
- Foundation for FinOps and AIOps systems

---

## 🏗️ Architecture

```text
GitHub Actions (Scheduler)
        ↓
Python Automation (GitHub Runner)
        ↓
Azure SDK (Compute + Monitor)
        ↓
VM Discovery + Metrics Query
        ↓
Utilization Analysis
        ↓
Decision Engine
        ↓
┌─────────────────────────────┬──────────────────────────────┐
│ JSON Report (Artifact)      │ Telegram Notification        │
│ Azure VM Tagging            │ VM Shutdown (optional)       │
└─────────────────────────────┴──────────────────────────────┘
```
---

## 📁 Project Structure

```text
azure-automation-tools/
│
├── automation/
│   ├── all_vm_metrics.py
│   ├── tag_vm_optimization.py
│   ├── shutdown_idle_vms.py
│   └── format_telegram_message.py
│
├── core/
│   ├── azure_clients.py
│   ├── config.py
│   ├── metrics.py
│   ├── tagging.py
│   ├── vm_actions.py
│   └── reporting.py
│
├── .github/workflows/
│   └── azure_automation.yml
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
    AZURE_SUBSCRIPTION_ID=your-subscription-id
    DRY_RUN=true
    CPU_LOOKBACK_MINUTES=30
    MIN_SAMPLE_COUNT=10
    PROTECTION_TAG_NAME=doNotShutdown
    PROTECTION_TAG_VALUE=true
   ```
3. Authenticate to Azure
   ```bash
   az login
   ```
4. Run

   ```bash
   python3 -m automation.shutdown_idle_vms
   ```
   
## ⚙️ GitHub Actions Setup

Required Secrets
```text
AZURE_CREDENTIALS
AZURE_SUBSCRIPTION_ID
TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID
```

## 📊 Example Output

```bash
Analyzing VM: test-vm-automation
  Samples: 24
  Avg CPU: 3.88
  Status: IDLE
  Decision: SHUTDOWN CANDIDATE
```

## 📄 Example Report

```bash
{
  "vm_name": "test-vm-automation",
  "average_cpu_percent": 3.88,
  "sample_count": 24,
  "status": "IDLE",
  "decision": "SHUTDOWN CANDIDATE",
  "dry_run": false
}
```

## 🔒 Safety Mechanisms

- Dry-run mode (```DRY_RUN=true```)
- Protection tag override (```doNotShutdown=true```)
- Minimum sample validation
- Separation of decision and execution logic

## 🧠 Key Concepts Demonstrated

- Azure SDK integration
- Azure Monitor metrics querying
- Infrastructure utilization analysis
- FinOps-style cost optimization
- CI/CD-driven automation (GitHub Actions)
- Safe automation patterns (dry-run + override)
- Modular Python architecture

## 🔮 Future Improvements

- Session-aware analysis (since last boot)
- Multi-run confirmation before shutdown
- Time-based policies (e.g. off-hours shutdown)
- Support for additional metrics (memory, disk, network)
- Dashboard / visualization layer
- Migration to serverless (Azure Functions)
- AI-based anomaly detection

## 🎯 Goal

To build production-style Azure automation tools while strengthening skills in:

- Cloud engineering
- DevOps & CI/CD
- Infrastructure automation
- Observability & FinOps
- AI-assisted operations
   
