"""Azure AI Search vector adapter with a safe local fallback."""
import os

class AzureAISearchVectorStore:
    def __init__(self):
        self.endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        self.index = os.getenv("AZURE_SEARCH_INDEX", "cloud-knowledge")
    def configured(self): return bool(self.endpoint)
    def search(self, query: str, top_k: int = 5):
        if not self.configured():
            return [{"content": "Azure AI Search is not configured; using local RAG fallback.", "score": 0.0}]
        try:
            from azure.identity import DefaultAzureCredential
            from azure.search.documents import SearchClient
            client = SearchClient(self.endpoint, self.index, DefaultAzureCredential())
            return [{"content": r.get("content", ""), "score": r.get("@search.score", 0)} for r in client.search(query, top=top_k)]
        except Exception as exc:
            return [{"content": f"Search adapter unavailable: {exc}", "score": 0.0}]
