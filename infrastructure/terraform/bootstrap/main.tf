resource "random_string" "suffix" {
  length  = 6
  special = false
  upper   = false
}

resource "azurerm_resource_group" "tfstate" {
  name     = "rg-uptimehub-tfstate"
  location = "polandcentral"
}

# DEV EXCEPTION:
# Terraform state is accessed by Microsoft-hosted Azure DevOps agents whose
# outbound IP addresses are not fixed for this project.
# Authentication and authorization are enforced through Azure AD/RBAC.
# The state container is private, TLS 1.2+ is required, and blob versioning
# is enabled.
# Production hardening: move state access to a private endpoint with an
# appropriately networked agent before enforcing default_action = "Deny".
resource "azurerm_storage_account" "tfstate" {
  name                     = "uptimehubtf${random_string.suffix.result}"
  resource_group_name      = azurerm_resource_group.tfstate.name
  location                 = azurerm_resource_group.tfstate.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  min_tls_version = "TLS1_2"

  blob_properties {
    versioning_enabled = true
  }

  tags = {
    project     = "UptimeHub"
    environment = "shared"
    managed_by  = "Terraform"
    purpose     = "Terraform State"
  }
}

resource "azurerm_storage_container" "tfstate" {
  name                  = "tfstate"
  storage_account_id    = azurerm_storage_account.tfstate.id
  container_access_type = "private"
}
