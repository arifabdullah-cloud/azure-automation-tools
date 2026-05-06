# Azure Lab Infrastructure (Bicep)

This folder contains Bicep templates for deploying a small Azure VM lab environment used by the Azure Automation Tools project.

---

## Prerequisites

- Azure CLI installed
- Logged in to Azure
- SSH public key available

## Login to Azure:

```bash
az login
```

## SSH Public Key

Get your existing SSH public key:

```bash
cat ~/.ssh/id_rsa.pub
```

If you do not have one:

```bash
ssh-keygen -t rsa -b 4096 -C "azure-automation-tools"
```

Update:

```bash
parameters.dev.json
```

Replace:

```bash
"sshPublicKey": {  "value": "REPLACE_WITH_SSH_PUBLIC_KEY"}
```

with your real SSH public key.

## Create Resource Group

```bash
az group create \
  --name TEST-VM-AUTOMATION_GROUP \
  --location malaysiawest
```

## Deploy Infrastructure

```bash
az deployment group create \
  --resource-group TEST-VM-AUTOMATION_GROUP \
  --template-file infrastructure/bicep/main.bicep \
  --parameters @infrastructure/bicep/parameters.dev.json
```

## Connect to VM

```bash
ssh azureuser@<public-ip-address>
```

## Destroy Infrastructure

Delete the full resource group to avoid ongoing Azure cost:

```bash
az group delete \
  --name TEST-VM-AUTOMATION_GROUP \
  --yes \
  --no-wait
```
