resource "azurerm_postgresql_flexible_server" "this" {
  zone                = "3"
  name                = "psql-uptimehub-${var.environment}"
  resource_group_name = var.resource_group_name
  location            = var.location

  version = "16"

  administrator_login    = var.administrator_login
  administrator_password = var.administrator_password

  delegated_subnet_id = var.delegated_subnet_id
  private_dns_zone_id = var.private_dns_zone_id

  sku_name   = "B_Standard_B1ms"
  storage_mb = 32768

  backup_retention_days        = 7
  geo_redundant_backup_enabled = false

  public_network_access_enabled = false

  tags = {
    project     = "UptimeHub"
    environment = var.environment
    managed_by  = "Terraform"
  }
}

resource "azurerm_postgresql_flexible_server_database" "uptimehub" {
  name      = "uptimehub"
  server_id = azurerm_postgresql_flexible_server.this.id

  charset   = "UTF8"
  collation = "en_US.utf8"
}
