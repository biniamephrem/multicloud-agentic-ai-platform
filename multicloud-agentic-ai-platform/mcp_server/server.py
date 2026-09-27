"""Minimal MCP-style tool registry. Adapt handlers to the official MCP SDK for production."""
TOOLS={
 'cloud_inventory': {'description':'Return sanitized cloud resource inventory','write':False},
 'terraform_plan': {'description':'Run/inspect an IaC plan','write':False},
 'apply_terraform': {'description':'Apply approved IaC change','write':True},
}
def list_tools(): return TOOLS
def call_tool(name,args=None,approved=False):
    tool=TOOLS[name]
    if tool['write'] and not approved: return {'status':'approval_required','tool':name}
    return {'status':'ok','tool':name,'args':args or {},'result':'demo result'}
