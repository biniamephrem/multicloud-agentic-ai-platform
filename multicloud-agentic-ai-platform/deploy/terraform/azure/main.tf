terraform { required_version = ">= 1.6.0" }
variable "location" { default = "eastus2" }
variable "resource_group_name" { default = "rg-agentic-ai-demo" }
resource "azurerm_resource_group" "this" { name = var.resource_group_name location = var.location }
# Extend with Azure OpenAI, AI Search, Key Vault, Container Apps and private endpoints.
