output "id" {
  description = "Azure Managed Redis ID"
  value       = azurerm_managed_redis.this.id
}

output "name" {
  description = "Azure Managed Redis name"
  value       = azurerm_managed_redis.this.name
}

output "hostname" {
  description = "Azure Managed Redis hostname"
  value       = azurerm_managed_redis.this.hostname
}

output "port" {
  description = "Azure Managed Redis encrypted port"
  value       = azurerm_managed_redis.this.default_database[0].port
}
