terraform {
  required_version = ">= 1.6.0"
  required_providers {
    azurerm = { source = "hashicorp/azurerm", version = "~> 4.0" }
    random  = { source = "hashicorp/random", version = "~> 3.6" }
  }
}
provider "azurerm" { features {} }

data "azurerm_client_config" "current" {}
variable "location" { type=string; default="eastus2" }
variable "prefix" { type=string; default="agentic-ai" }
variable "environment" { type=string; default="dev" }
variable "container_image" { type=string; default="mcr.microsoft.com/azuredocs/containerapps-helloworld:latest" }
variable "openai_deployment" { type=string; default="gpt-5-mini" }
variable "openai_model_name" { type=string; default="gpt-5-mini" }
variable "openai_model_version" { type=string; default="2025-08-07" }
variable "deploy_model" { type=bool; default=false }

resource "random_string" "suffix" { length=6; special=false; upper=false }
locals { name="${var.prefix}-${var.environment}-${random_string.suffix.result}" }
resource "azurerm_resource_group" "this" { name="rg-${local.name}"; location=var.location }
resource "azurerm_log_analytics_workspace" "this" { name="log-${local.name}"; location=var.location; resource_group_name=azurerm_resource_group.this.name; sku="PerGB2018"; retention_in_days=30 }
resource "azurerm_application_insights" "this" { name="appi-${local.name}"; location=var.location; resource_group_name=azurerm_resource_group.this.name; workspace_id=azurerm_log_analytics_workspace.this.id; application_type="web" }
resource "azurerm_container_registry" "this" { name=replace("acr${local.name}","-",""); resource_group_name=azurerm_resource_group.this.name; location=var.location; sku="Basic"; admin_enabled=false }
resource "azurerm_user_assigned_identity" "app" { name="id-${local.name}"; resource_group_name=azurerm_resource_group.this.name; location=var.location }
resource "azurerm_key_vault" "this" { name=substr(replace("kv-${local.name}","_","-"),0,24); location=var.location; resource_group_name=azurerm_resource_group.this.name; tenant_id=data.azurerm_client_config.current.tenant_id; sku_name="standard"; enable_rbac_authorization=true; purge_protection_enabled=true }
resource "azurerm_search_service" "this" { name="srch-${local.name}"; resource_group_name=azurerm_resource_group.this.name; location=var.location; sku="basic"; local_authentication_enabled=false; identity { type="SystemAssigned" } }
resource "azurerm_cognitive_account" "openai" { name="aoai-${local.name}"; location=var.location; resource_group_name=azurerm_resource_group.this.name; kind="OpenAI"; sku_name="S0"; custom_subdomain_name="aoai-${local.name}"; local_auth_enabled=false }
resource "azurerm_cognitive_deployment" "model" { count=var.deploy_model ? 1 : 0; name=var.openai_deployment; cognitive_account_id=azurerm_cognitive_account.openai.id; model { format="OpenAI"; name=var.openai_model_name; version=var.openai_model_version }; sku { name="GlobalStandard"; capacity=10 } }
resource "azurerm_container_app_environment" "this" { name="cae-${local.name}"; location=var.location; resource_group_name=azurerm_resource_group.this.name; log_analytics_workspace_id=azurerm_log_analytics_workspace.this.id }
resource "azurerm_role_assignment" "acr" { scope=azurerm_container_registry.this.id; role_definition_name="AcrPull"; principal_id=azurerm_user_assigned_identity.app.principal_id }
resource "azurerm_role_assignment" "openai" { scope=azurerm_cognitive_account.openai.id; role_definition_name="Cognitive Services OpenAI User"; principal_id=azurerm_user_assigned_identity.app.principal_id }
resource "azurerm_role_assignment" "search" { scope=azurerm_search_service.this.id; role_definition_name="Search Index Data Reader"; principal_id=azurerm_user_assigned_identity.app.principal_id }
resource "azurerm_role_assignment" "kv" { scope=azurerm_key_vault.this.id; role_definition_name="Key Vault Secrets User"; principal_id=azurerm_user_assigned_identity.app.principal_id }
resource "azurerm_container_app" "api" {
  name="ca-${local.name}"; container_app_environment_id=azurerm_container_app_environment.this.id; resource_group_name=azurerm_resource_group.this.name; revision_mode="Single"
  identity { type="UserAssigned"; identity_ids=[azurerm_user_assigned_identity.app.id] }
  registry { server=azurerm_container_registry.this.login_server; identity=azurerm_user_assigned_identity.app.id }
  template {
    min_replicas=1; max_replicas=3
    container {
      name="api"; image=var.container_image; cpu=0.5; memory="1Gi"
      env { name="LLM_PROVIDER"; value="azure" }
      env { name="AZURE_CLIENT_ID"; value=azurerm_user_assigned_identity.app.client_id }
      env { name="AZURE_OPENAI_ENDPOINT"; value=azurerm_cognitive_account.openai.endpoint }
      env { name="AZURE_OPENAI_DEPLOYMENT"; value=var.openai_deployment }
      env { name="AZURE_SEARCH_ENDPOINT"; value="https://${azurerm_search_service.this.name}.search.windows.net" }
      env { name="APPLICATIONINSIGHTS_CONNECTION_STRING"; value=azurerm_application_insights.this.connection_string }
      liveness_probe { transport="HTTP"; port=8000; path="/health"; initial_delay=10; interval_seconds=30 }
      readiness_probe { transport="HTTP"; port=8000; path="/health"; interval_seconds=10 }
    }
  }
  ingress { external_enabled=true; target_port=8000; traffic_weight { percentage=100; latest_revision=true } }
  depends_on=[azurerm_role_assignment.acr,azurerm_role_assignment.openai,azurerm_role_assignment.search]
}
output "resource_group" { value=azurerm_resource_group.this.name }
output "acr_login_server" { value=azurerm_container_registry.this.login_server }
output "app_url" { value="https://${azurerm_container_app.api.latest_revision_fqdn}" }
output "openai_endpoint" { value=azurerm_cognitive_account.openai.endpoint }
output "search_endpoint" { value="https://${azurerm_search_service.this.name}.search.windows.net" }
