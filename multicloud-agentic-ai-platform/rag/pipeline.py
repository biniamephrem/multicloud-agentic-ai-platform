from pathlib import Path
import re, math
from collections import Counter

class SimpleRAG:
    """Dependency-light reference RAG. Replace retrieval with AI Search/OpenSearch/Vertex Vector Search."""
    def __init__(self, knowledge_dir='knowledge'):
        self.docs=[]
        for p in Path(knowledge_dir).glob('**/*.md'):
            text=p.read_text(encoding='utf-8')
            for i, chunk in enumerate(re.split(r'\n\s*\n', text)):
                if chunk.strip(): self.docs.append({'id':f'{p.name}:{i}','text':chunk.strip()})
    def _tokens(self,s): return re.findall(r'[a-z0-9_-]+',s.lower())
    def search(self, query, k=4):
        q=Counter(self._tokens(query)); scored=[]
        for d in self.docs:
            x=Counter(self._tokens(d['text']))
            dot=sum(q[t]*x[t] for t in q); nq=math.sqrt(sum(v*v for v in q.values())); nx=math.sqrt(sum(v*v for v in x.values()))
            score=dot/(nq*nx) if nq and nx else 0
            scored.append((score,d))
        return [dict(d,score=round(s,3)) for s,d in sorted(scored,key=lambda z:z[0],reverse=True)[:k]]
