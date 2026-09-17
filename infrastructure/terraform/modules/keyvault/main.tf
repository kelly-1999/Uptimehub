data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "this" {
  name                = var.key_vault_name
  location            = var.location
  resource_group_name = var.resource_group_name
  tenant_id           = data.azurerm_client_config.current.tenant_id

  sku_name = "standard"

  rbac_authorization_enabled    = true
  soft_delete_retention_days    = 7
  purge_protection_enabled      = false
  public_network_access_enabled = false

  tags = {
    project     = "UptimeHub"
    environment = var.environment
    managed_by  = "Terraform"
  }
}

resource "azurerm_user_assigned_identity" "uptimehub" {
  name                = "id-uptimehub-${var.environment}"
  location            = var.location
  resource_group_name = var.resource_group_name

  tags = {
    project     = "UptimeHub"
    environment = var.environment
    managed_by  = "Terraform"
  }
}

resource "azurerm_role_assignment" "keyvault_secrets_user" {
  scope                = azurerm_key_vault.this.id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = azurerm_user_assigned_identity.uptimehub.principal_id
}

resource "azurerm_federated_identity_credential" "uptimehub" {
  name                      = "fic-uptimehub-${var.environment}"
  user_assigned_identity_id = azurerm_user_assigned_identity.uptimehub.id

  audience = [
    "api://AzureADTokenExchange"
  ]

  issuer = var.aks_oidc_issuer_url

  subject = "system:serviceaccount:uptimehub-dev:uptimehub-app"
}
