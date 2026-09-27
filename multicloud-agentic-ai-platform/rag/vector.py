"""Production extension point for managed vector search.
Local demo remains dependency-light; this interface allows Azure AI Search,
Amazon OpenSearch, or Vertex/other vector stores without changing agents.
"""
from dataclasses import dataclass
from typing import Protocol
@dataclass
class Hit: id:str; text:str; score:float; source:str="knowledge"
class Retriever(Protocol):
    def search(self,query:str,k:int=4)->list[dict]: ...
