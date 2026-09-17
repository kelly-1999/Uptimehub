variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
}

variable "location" {
  description = "Azure region"
  type        = string
}

variable "environment" {
  description = "Deployment environment"
  type        = string
}

variable "administrator_login" {
  description = "PostgreSQL administrator username"
  type        = string
  default     = "uptimehubadmin"
}

variable "administrator_password" {
  description = "PostgreSQL administrator password"
  type        = string
  sensitive   = true
}

variable "private_dns_zone_id" {
  description = "ID of the PostgreSQL private DNS zone"
  type        = string
}

variable "delegated_subnet_id" {
  description = "ID of the subnet delegated to PostgreSQL Flexible Server"
  type        = string
}
