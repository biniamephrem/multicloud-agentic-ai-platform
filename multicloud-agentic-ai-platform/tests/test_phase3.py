from state.checkpoint import CheckpointStore
from evaluation.advanced_eval import evaluate
from rag.azure_ai_search import AzureAISearchVectorStore
from cloud_tools.read_only import AzureReadOnlyTools, AWSReadOnlyTools, GCPReadOnlyTools

def test_checkpoint(tmp_path):
    s=CheckpointStore(str(tmp_path/'c.db')); s.put('t1', {'x':1}); assert s.get('t1')['x']==1

def test_eval():
    r=evaluate('azure private endpoint','azure private endpoint uses private connectivity','azure private endpoint uses private connectivity and private dns')
    assert r.safety==1 and r.passed

def test_search_fallback(monkeypatch):
    monkeypatch.delenv('AZURE_SEARCH_ENDPOINT', raising=False)
    assert AzureAISearchVectorStore().search('x')[0]['score']==0

def test_cloud_tools_safe_without_credentials():
    assert AzureReadOnlyTools().list_resources().provider=='azure'
    assert AWSReadOnlyTools().list_regions().provider=='aws'
    assert GCPReadOnlyTools().list_projects().provider=='gcp'
