resource "azurerm_managed_redis" "this" {
  name                = var.redis_name
  resource_group_name = var.resource_group_name
  location            = var.location

  sku_name                  = "Balanced_B0"
  high_availability_enabled = false
  public_network_access     = "Disabled"

  default_database {
    access_keys_authentication_enabled = true
    client_protocol                    = "Encrypted"
  }

  tags = {
    project     = "UptimeHub"
    environment = var.environment
    managed_by  = "Terraform"
  }
}
