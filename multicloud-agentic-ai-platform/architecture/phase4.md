# Phase 4 — Azure live deployment architecture

```mermaid
flowchart LR
 U[User / API Client] --> CA[Azure Container Apps\nFastAPI + LangGraph]
 CA --> GR[Guardrails]
 GR --> SUP[Supervisor / Multi-Agent]
 SUP --> RAG[RAG]
 SUP --> MCP[MCP tool boundary]
 SUP --> A2A[A2A endpoint]
 RAG --> AIS[Azure AI Search]
 SUP --> AOAI[Azure OpenAI\nResponses API]
 CA --> APP[Application Insights / OpenTelemetry]
 MI[User-assigned Managed Identity] -. Entra ID .-> CA
 MI -. RBAC .-> AOAI
 MI -. RBAC .-> AIS
 MI -. RBAC .-> KV[Key Vault]
 ACR[Azure Container Registry] --> CA
 GH[GitHub Actions] --> ACR
 GH --> TF[Terraform]
 TF --> CA
```

## Security baseline
- Managed identity is the default application credential; no Azure OpenAI API key is required.
- Azure OpenAI local authentication is disabled in Terraform.
- AI Search local authentication is disabled.
- MCP cloud actions remain read-only by default; write/destructive operations require an explicit approval boundary.
- Production hardening: add VNet integration/private endpoints, private DNS, WAF/API gateway, Defender, diagnostic settings, and environment-specific policy controls.
