import re
BLOCKED_PATTERNS=[r'ignore (all|previous) instructions',r'reveal .*secret',r'dump .*credentials']
WRITE_TOOLS={'delete_resource','apply_terraform','rotate_key','modify_firewall'}
def check_input(text:str):
    for p in BLOCKED_PATTERNS:
        if re.search(p,text,re.I): return False,'Possible prompt injection or secret-exfiltration request.'
    return True,'ok'
def authorize_tool(tool:str, approved:bool=False):
    return (tool not in WRITE_TOOLS) or approved
