"""Read-only cloud inventory adapters. Real SDK calls are enabled only when credentials exist."""
from dataclasses import dataclass
from typing import Any

@dataclass
class ToolResult:
    provider: str
    operation: str
    data: Any
    mode: str = "demo"

class AzureReadOnlyTools:
    def list_resources(self) -> ToolResult:
        try:
            from azure.identity import DefaultAzureCredential
            from azure.mgmt.resource import ResourceManagementClient
            import os
            sub = os.environ["AZURE_SUBSCRIPTION_ID"]
            items = [r.as_dict() for r in ResourceManagementClient(DefaultAzureCredential(), sub).resources.list()]
            return ToolResult("azure", "list_resources", items, "live")
        except Exception as exc:
            return ToolResult("azure", "list_resources", {"demo": True, "reason": str(exc)[:160]})

class AWSReadOnlyTools:
    def list_regions(self) -> ToolResult:
        try:
            import boto3
            data = boto3.client("ec2").describe_regions(AllRegions=False)["Regions"]
            return ToolResult("aws", "list_regions", data, "live")
        except Exception as exc:
            return ToolResult("aws", "list_regions", {"demo": True, "reason": str(exc)[:160]})

class GCPReadOnlyTools:
    def list_projects(self) -> ToolResult:
        try:
            from google.cloud import resourcemanager_v3
            client = resourcemanager_v3.ProjectsClient()
            data = [{"name": p.name, "project_id": p.project_id} for p in client.search_projects()]
            return ToolResult("gcp", "list_projects", data, "live")
        except Exception as exc:
            return ToolResult("gcp", "list_projects", {"demo": True, "reason": str(exc)[:160]})
