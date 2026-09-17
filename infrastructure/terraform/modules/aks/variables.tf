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

variable "aks_subnet_id" {
  description = "ID of the subnet used by AKS"
  type        = string
}

variable "acr_id" {
  description = "ID of the Azure Container Registry"
  type        = string
}

variable "node_count" {
  description = "Initial number of AKS nodes"
  type        = number
  default     = 1
}

variable "node_vm_size" {
  description = "VM size used by the AKS node pool"
  type        = string
  default     = "Standard_D2s_v5"
}
