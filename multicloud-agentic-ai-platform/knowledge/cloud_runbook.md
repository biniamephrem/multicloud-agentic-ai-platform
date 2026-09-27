# Multi-Cloud Operations Runbook
Azure private workloads should prefer Private Endpoint/Private Link and centralized DNS. AWS workloads should use least-privilege IAM, private subnets for application tiers, centralized logging, and controlled egress. GCP workloads should use least-privilege IAM and private service connectivity where appropriate.

## Incident workflow
1. Identify affected service and scope. 2. Retrieve approved architecture/runbook. 3. Inspect read-only telemetry and configuration. 4. Correlate network, identity and service health. 5. Propose remediation. 6. Require human approval for destructive or write operations.

## IaC
Production infrastructure changes should be made through reviewed infrastructure-as-code pipelines. Run plan/what-if before apply and preserve audit evidence.
