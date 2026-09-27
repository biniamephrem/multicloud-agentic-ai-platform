# Phase 4: Live Azure Deployment

Phase 4 turns the portfolio into a deployable Azure-first reference implementation.

## What is new
1. Azure OpenAI **v1 Responses API** provider using `OpenAI(base_url=.../openai/v1/)`.
2. **Microsoft Entra ID / Managed Identity** authentication by default; API key is only an optional local fallback.
3. Terraform for Resource Group, Container Apps, ACR, Azure OpenAI, Azure AI Search, Key Vault, Log Analytics, Application Insights, managed identity, and RBAC.
4. GitHub Actions test + Terraform validation/plan workflow with OIDC login and an intentional approval boundary before apply.
5. Container Apps health probes and production environment variables.
6. Architecture/security documentation for live deployment.

## Deploy
```bash
cd deployment/azure
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform fmt -check
terraform validate
terraform plan
terraform apply
```

The initial Terraform uses a placeholder image. After ACR exists, build and push this application image, update `container_image`, then apply again.

```bash
export ACR_NAME=<your-acr-name>
./scripts/deploy_azure.sh
```

## Important model note
Azure model availability, deployment SKU, capacity, and model version vary by region and subscription. The Terraform therefore defaults `deploy_model=false`. Confirm the model available to your subscription, then set the deployment variables and enable model deployment.

## Production hardening path
The baseline is deliberately observable and easy to demo. For a government/enterprise production landing zone, extend it with VNet-integrated Container Apps, Private Endpoints for Azure OpenAI/Search/Key Vault/ACR, Private DNS, ingress through an approved WAF/API gateway, centralized diagnostic settings/SIEM, policy-as-code, customer-managed keys where required, and separate dev/test/prod subscriptions.
