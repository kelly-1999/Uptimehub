terraform {
  required_version = ">= 1.10.0"

  required_providers {
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }

    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }

  backend "azurerm" {}
}
