# Azure Lab Infrastructure

This folder contains Bicep templates for deploying a small Azure VM lab used by the Azure automation tools project.

## Resources Created

- Virtual Network
- Subnet
- Network Security Group allowing SSH
- Public IP
- Network Interface
- Ubuntu Linux VM

## Deploy

Create the resource group:

```bash
az group create \
  --name TEST-VM-AUTOMATION_GROUP \
  --location malaysiawest
