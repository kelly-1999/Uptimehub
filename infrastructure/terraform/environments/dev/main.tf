resource "azurerm_resource_group" "uptimehub" {
  name     = "rg-uptimehub-dev"
  location = "polandcentral"

  tags = {
    project     = "UptimeHub"
    environment = "dev"
    managed_by  = "Terraform"
  }
}

module "networking" {

  postgresql_subnet_prefixes = [
    "10.10.18.0/24"
  ]

  source = "../../modules/networking"

  resource_group_name = azurerm_resource_group.uptimehub.name
  location            = azurerm_resource_group.uptimehub.location
  environment         = "dev"

  vnet_address_space = [
    "10.10.0.0/16"
  ]

  aks_subnet_prefixes = [
    "10.10.0.0/20"
  ]

  appgateway_subnet_prefixes = [
    "10.10.16.0/24"
  ]

  private_endpoints_subnet_prefixes = [
    "10.10.17.0/24"
  ]
}

resource "azurerm_private_dns_zone" "postgresql" {
  name                = "uptimehub-dev.postgres.database.azure.com"
  resource_group_name = azurerm_resource_group.uptimehub.name

  tags = {
    project     = "UptimeHub"
    environment = "dev"
    managed_by  = "Terraform"
  }
}

resource "azurerm_private_dns_zone_virtual_network_link" "postgresql" {
  name                  = "link-uptimehub-dev-postgresql"
  resource_group_name   = azurerm_resource_group.uptimehub.name
  private_dns_zone_name = azurerm_private_dns_zone.postgresql.name
  virtual_network_id    = module.networking.vnet_id

  registration_enabled = false
}


resource "random_string" "acr_suffix" {
  length  = 6
  special = false
  upper   = false
}

module "acr" {
  source = "../../modules/acr"

  resource_group_name = azurerm_resource_group.uptimehub.name
  location            = azurerm_resource_group.uptimehub.location
  environment         = "dev"

  acr_name = "acruptimehub${random_string.acr_suffix.result}"
}

module "aks" {
  source = "../../modules/aks"

  resource_group_name = azurerm_resource_group.uptimehub.name
  location            = azurerm_resource_group.uptimehub.location
  environment         = "dev"

  aks_subnet_id = module.networking.aks_subnet_id
  acr_id        = module.acr.id

  node_count   = 1
  node_vm_size = "Standard_D2s_v5"
}

module "postgresql" {
  source = "../../modules/postgresql"

  resource_group_name = azurerm_resource_group.uptimehub.name
  location            = azurerm_resource_group.uptimehub.location
  environment         = "dev"

  administrator_login    = "uptimehubadmin"
  administrator_password = var.postgresql_admin_password

  delegated_subnet_id = module.networking.postgresql_subnet_id
  private_dns_zone_id = azurerm_private_dns_zone.postgresql.id

  depends_on = [
    azurerm_private_dns_zone_virtual_network_link.postgresql
  ]
}

module "redis" {
  source = "../../modules/redis"

  resource_group_name = azurerm_resource_group.uptimehub.name
  location            = azurerm_resource_group.uptimehub.location
  environment         = "dev"

  redis_name = "redis-uptimehub-dev"
}
resource "azurerm_private_dns_zone" "redis" {
  name                = "privatelink.redis.azure.net"
  resource_group_name = azurerm_resource_group.uptimehub.name

  tags = {
    project     = "UptimeHub"
    environment = "dev"
    managed_by  = "Terraform"
  }
}

resource "azurerm_private_dns_zone_virtual_network_link" "redis" {
  name                  = "link-uptimehub-dev-redis"
  resource_group_name   = azurerm_resource_group.uptimehub.name
  private_dns_zone_name = azurerm_private_dns_zone.redis.name
  virtual_network_id    = module.networking.vnet_id

  registration_enabled = false
}

resource "azurerm_private_endpoint" "redis" {
  name                = "pe-redis-uptimehub-dev"
  location            = azurerm_resource_group.uptimehub.location
  resource_group_name = azurerm_resource_group.uptimehub.name
  subnet_id           = module.networking.private_endpoints_subnet_id

  private_service_connection {
    name                           = "psc-redis-uptimehub-dev"
    private_connection_resource_id = module.redis.id
    subresource_names              = ["redisEnterprise"]
    is_manual_connection           = false
  }

  private_dns_zone_group {
    name = "redis-private-dns"

    private_dns_zone_ids = [
      azurerm_private_dns_zone.redis.id
    ]
  }

  tags = {
    project     = "UptimeHub"
    environment = "dev"
    managed_by  = "Terraform"
  }
}

module "keyvault" {
  source = "../../modules/keyvault"

  resource_group_name = azurerm_resource_group.uptimehub.name
  location            = azurerm_resource_group.uptimehub.location
  environment         = "dev"

  key_vault_name      = "kv-uptimehub-${random_string.acr_suffix.result}"
  aks_oidc_issuer_url = module.aks.oidc_issuer_url
}

resource "azurerm_private_endpoint" "keyvault" {
  name                = "pe-kv-uptimehub-dev"
  location            = azurerm_resource_group.uptimehub.location
  resource_group_name = azurerm_resource_group.uptimehub.name
  subnet_id           = module.networking.private_endpoints_subnet_id

  private_service_connection {
    name                           = "psc-kv-uptimehub-dev"
    private_connection_resource_id = module.keyvault.key_vault_id
    subresource_names              = ["vault"]
    is_manual_connection           = false
  }

  private_dns_zone_group {
    name = "keyvault-private-dns"

    private_dns_zone_ids = [
      azurerm_private_dns_zone.keyvault.id
    ]
  }

  tags = {
    project     = "UptimeHub"
    environment = "dev"
    managed_by  = "Terraform"
  }
}


resource "azurerm_private_dns_zone" "keyvault" {
  name                = "privatelink.vaultcore.azure.net"
  resource_group_name = azurerm_resource_group.uptimehub.name

  tags = {
    project     = "UptimeHub"
    environment = "dev"
    managed_by  = "Terraform"
  }
}

resource "azurerm_private_dns_zone_virtual_network_link" "keyvault" {
  name                  = "link-uptimehub-dev-keyvault"
  resource_group_name   = azurerm_resource_group.uptimehub.name
  private_dns_zone_name = azurerm_private_dns_zone.keyvault.name
  virtual_network_id    = module.networking.vnet_id

  registration_enabled = false
}

module "appgateway" {
  source = "../../modules/appgateway"

  resource_group_name = azurerm_resource_group.uptimehub.name
  location            = azurerm_resource_group.uptimehub.location
  environment         = "dev"

  name      = "agw-uptimehub-dev"
  subnet_id = module.networking.appgateway_subnet_id
}

resource "azurerm_user_assigned_identity" "agic" {
  name                = "id-uptimehub-agic-dev"
  location            = azurerm_resource_group.uptimehub.location
  resource_group_name = azurerm_resource_group.uptimehub.name

  tags = {
    project     = "UptimeHub"
    environment = "dev"
    managed_by  = "Terraform"
  }
}

resource "azurerm_role_assignment" "agic_contributor" {
  scope                = module.appgateway.id
  role_definition_name = "Contributor"
  principal_id         = azurerm_user_assigned_identity.agic.principal_id
}
