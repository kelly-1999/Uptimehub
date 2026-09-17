output "vnet_name" {
  value = module.networking.vnet_name
}

output "aks_subnet_id" {
  value = module.networking.aks_subnet_id
}

output "acr_name" {
  value = module.acr.name
}

output "acr_login_server" {
  value = module.acr.login_server
}
output "aks_name" {
  value = module.aks.name
}

output "aks_id" {
  value = module.aks.id
}

output "postgresql_server_name" {
  value = module.postgresql.name
}

output "postgresql_fqdn" {
  value = module.postgresql.fqdn
}

output "postgresql_database_name" {
  value = module.postgresql.database_name
}

output "redis_name" {
  value = module.redis.name
}

output "redis_hostname" {
  value = module.redis.hostname
}

output "redis_port" {
  value = module.redis.port
}
output "aks_oidc_issuer_url" {
  value = module.aks.oidc_issuer_url
}
output "key_vault_name" {
  value = module.keyvault.key_vault_name
}

output "workload_identity_client_id" {
  value = module.keyvault.identity_client_id
}

output "appgateway_public_ip" {
  value = module.appgateway.public_ip
}

output "appgateway_name" {
  value = module.appgateway.name
}

output "agic_client_id" {
  value = azurerm_user_assigned_identity.agic.client_id
}
