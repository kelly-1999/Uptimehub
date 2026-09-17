variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
}

variable "location" {
  description = "Azure region for the networking resources"
  type        = string
}

variable "environment" {
  description = "Deployment environment"
  type        = string
}

variable "vnet_address_space" {
  description = "Address space for the virtual network"
  type        = list(string)
}

variable "aks_subnet_prefixes" {
  description = "Address prefixes for the AKS subnet"
  type        = list(string)
}

variable "appgateway_subnet_prefixes" {
  description = "Address prefixes for the Application Gateway subnet"
  type        = list(string)
}

variable "private_endpoints_subnet_prefixes" {
  description = "Address prefixes for the private endpoints subnet"
  type        = list(string)
}

variable "postgresql_subnet_prefixes" {
  description = "Address prefixes for the PostgreSQL delegated subnet"
  type        = list(string)
}
