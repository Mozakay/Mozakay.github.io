#!/usr/bin/env bash
# Unit 4: Provision an Azure Ubuntu VM, configure Nginx and verify operation.
# Azure CLI / Bash, Target region: India South Central
set -euo pipefail

RG="unit4-rg-india"
LOCATION="indiasouthcentral"
VM="unit4-vm"
SIZE="Standard_B1s"
IMAGE="Ubuntu2204"
ADMIN="azureuser"

log() { printf '[%s] %s\n' "$(date +%H:%M:%S)" "$*"; }
command -v az >/dev/null || { echo 'Azure CLI is required.' >&2; exit 1; }
az account show --output none || { echo 'Please sign in to Azure.' >&2; exit 1; }

# Check whether the virtual machine already exists.
if az vm show --resource-group "$RG" --name "$VM" --output none 2>/dev/null; then
  log "Existing VM found: $VM (no new resources will be created)."
else
  if ! az group exists --name "$RG" | grep -qx true; then
    log "Creating resource group: $RG"
    az group create --name "$RG" --location "$LOCATION" --output none
  fi
  log "Creating Ubuntu virtual machine: $VM"
  az vm create --resource-group "$RG" --name "$VM" \
    --location "$LOCATION" --image "$IMAGE" --size "$SIZE" \
    --admin-username "$ADMIN" --generate-ssh-keys \
    --public-ip-sku Standard --nsg-rule NONE --output none
fi

power=$(az vm get-instance-view --resource-group "$RG" --name "$VM" \
  --query "instanceView.statuses[?starts_with(code, 'PowerState/')].code | [0]" -o tsv)
if [[ "$power" != "PowerState/running" ]]; then
  echo "VM is not running ($power). Start it only if you intend to run configuration checks." >&2
  exit 1
fi

log 'Configuring Nginx and performing basic system checks via Azure Run Command'
output=$(az vm run-command invoke --resource-group "$RG" --name "$VM" \
  --command-id RunShellScript --scripts '
    set -e
    sudo apt-get update
    sudo apt-get install -y nginx curl
    sudo systemctl enable --now nginx
    echo "<h1>Azure Bash Automation Successful</h1>" | sudo tee /var/www/html/index.html
    echo "=== HOSTNAME ==="; hostname
    echo "=== OS ==="; uname -r
    echo "=== DISK ==="; df -h /
    echo "=== MEMORY ==="; free -m
    echo "=== NGINX STATUS ==="; systemctl is-active nginx
    echo "=== HTTP TEST ==="
    curl --fail --silent --show-error http://localhost/
    systemctl is-active --quiet nginx
    curl --fail --silent http://localhost/ | grep -q "Azure Bash Automation Successful"
    echo "UNIT4_VERIFICATION_PASSED"
  ' --query 'value[0].message' --output tsv)
printf '%s\n' "$output"
if [[ "$output" != *'UNIT4_VERIFICATION_PASSED'* ]]; then
  echo 'Remote configuration/verification did not report success.' >&2
  exit 1
fi
log 'Azure VM provisioning/configuration verification completed.'
log 'When finished, stop (deallocate) the VM to avoid ongoing compute charges.'
