output "vnet_id" {
  description = "ID of the UptimeHub virtual network"
  value       = azurerm_virtual_network.this.id
}

output "vnet_name" {
  description = "Name of the UptimeHub virtual network"
  value       = azurerm_virtual_network.this.name
}

output "aks_subnet_id" {
  description = "ID of the AKS subnet"
  value       = azurerm_subnet.aks.id
}

output "appgateway_subnet_id" {
  description = "ID of the Application Gateway subnet"
  value       = azurerm_subnet.appgateway.id
}

output "private_endpoints_subnet_id" {
  description = "ID of the private endpoints subnet"
  value       = azurerm_subnet.private_endpoints.id
}

output "aks_nsg_id" {
  description = "ID of the AKS subnet network security group"
  value       = azurerm_network_security_group.aks.id
}

output "postgresql_subnet_id" {
  description = "ID of the PostgreSQL delegated subnet"
  value       = azurerm_subnet.postgresql.id
}
