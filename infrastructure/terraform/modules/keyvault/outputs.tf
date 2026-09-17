output "key_vault_id" {
  value = azurerm_key_vault.this.id
}

output "key_vault_name" {
  value = azurerm_key_vault.this.name
}

output "identity_id" {
  value = azurerm_user_assigned_identity.uptimehub.id
}

output "identity_client_id" {
  value = azurerm_user_assigned_identity.uptimehub.client_id
}

output "identity_principal_id" {
  value = azurerm_user_assigned_identity.uptimehub.principal_id
}
