from pathlib import Path

def test_azure_deployment_files_exist():
    assert Path('deployment/azure/main.tf').exists()
    assert Path('.github/workflows/azure-deploy.yml').exists()

def test_phase4_uses_identity_first_azure_openai():
    text=Path('llm/providers.py').read_text()
    assert 'get_bearer_token_provider' in text
    assert '/openai/v1/' in text
    assert 'responses.create' in text

def test_terraform_security_baseline():
    text=Path('deployment/azure/main.tf').read_text()
    assert 'local_auth_enabled=false' in text
    assert 'local_authentication_enabled=false' in text
    assert 'Cognitive Services OpenAI User' in text
    assert 'Search Index Data Reader' in text
