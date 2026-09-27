import os
from typing import Protocol

class LLMProvider(Protocol):
    def generate(self, system: str, user: str) -> str: ...

class LocalProvider:
    def generate(self, system: str, user: str) -> str:
        return f"{user}\n\n[Local demo mode: set LLM_PROVIDER=azure and Azure settings for live inference.]"

class AzureOpenAIProvider:
    """Azure OpenAI v1 Responses API with Entra ID by default; API key is optional."""
    def __init__(self):
        from openai import OpenAI
        endpoint=os.environ["AZURE_OPENAI_ENDPOINT"].rstrip("/")
        self.deployment=os.environ["AZURE_OPENAI_DEPLOYMENT"]
        api_key=os.getenv("AZURE_OPENAI_API_KEY")
        if api_key:
            credential=api_key
        else:
            from azure.identity import DefaultAzureCredential, get_bearer_token_provider
            credential=get_bearer_token_provider(DefaultAzureCredential(), "https://ai.azure.com/.default")
        self.client=OpenAI(base_url=f"{endpoint}/openai/v1/", api_key=credential)

    def generate(self, system: str, user: str) -> str:
        r=self.client.responses.create(model=self.deployment,instructions=system,input=user,max_output_tokens=1200)
        return r.output_text or ""

class BedrockProvider:
    def __init__(self):
        import boto3
        self.client=boto3.client("bedrock-runtime",region_name=os.getenv("AWS_REGION","us-east-1")); self.model=os.environ["BEDROCK_MODEL_ID"]
    def generate(self,system,user):
        r=self.client.converse(modelId=self.model,system=[{"text":system}],messages=[{"role":"user","content":[{"text":user}]}],inferenceConfig={"temperature":0.1,"maxTokens":1200})
        return r["output"]["message"]["content"][0]["text"]

class VertexProvider:
    def __init__(self):
        from google import genai
        self.client=genai.Client(vertexai=True,project=os.environ["GOOGLE_CLOUD_PROJECT"],location=os.getenv("GOOGLE_CLOUD_LOCATION","global")); self.model=os.getenv("VERTEX_MODEL","gemini-2.5-flash")
    def generate(self,system,user):
        r=self.client.models.generate_content(model=self.model,contents=f"SYSTEM: {system}\nUSER: {user}")
        return r.text or ""

def get_provider():
    name=os.getenv("LLM_PROVIDER","local").lower()
    return {"azure":AzureOpenAIProvider,"bedrock":BedrockProvider,"vertex":VertexProvider}.get(name,LocalProvider)()
