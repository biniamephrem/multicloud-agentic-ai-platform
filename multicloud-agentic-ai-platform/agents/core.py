from dataclasses import dataclass
from rag.pipeline import SimpleRAG
from guardrails.policy import check_input

@dataclass
class AgentResult:
    agent:str; answer:str; evidence:list

class SpecialistAgent:
    def __init__(self,name,keywords,rag): self.name=name; self.keywords=keywords; self.rag=rag
    def run(self,question):
        evidence=self.rag.search(question)
        context=' | '.join(x['text'] for x in evidence[:2])
        return AgentResult(self.name,f'[{self.name}] Analysis for: {question}\nGrounded context: {context}\nRecommended next step: validate read-only telemetry/configuration, then propose an IaC-reviewed remediation.',evidence)

class Supervisor:
    def __init__(self):
        rag=SimpleRAG(); self.rag=rag
        self.agents=[SpecialistAgent('Azure Agent',['azure','vnet','nsg','private endpoint'],rag),SpecialistAgent('AWS Agent',['aws','vpc','iam','tgw','s3'],rag),SpecialistAgent('GCP Agent',['gcp','gke','vpc','vertex'],rag),SpecialistAgent('Security Agent',['security','iam','rbac','guardrail','kms'],rag),SpecialistAgent('Terraform Agent',['terraform','iac','plan','module'],rag)]
    def route(self,q):
        ok,msg=check_input(q)
        if not ok: return {'blocked':True,'reason':msg}
        chosen=[a for a in self.agents if any(k in q.lower() for k in a.keywords)] or [self.agents[3]]
        results=[a.run(q) for a in chosen[:3]]
        return {'blocked':False,'agents':[r.agent for r in results],'answer':'\n\n'.join(r.answer for r in results),'citations':[e['id'] for r in results for e in r.evidence[:2]]}
