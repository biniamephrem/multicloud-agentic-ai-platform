from agents.core import Supervisor
DATASET=[('How should Azure private access be designed?','Private'),('What is the incident workflow?','telemetry'),('How should production changes be made?','infrastructure-as-code')]
def run_eval():
    s=Supervisor(); passed=0; rows=[]
    for q,needle in DATASET:
        out=s.route(q); ok=needle.lower() in out['answer'].lower(); passed+=ok; rows.append({'question':q,'pass':ok})
    return {'score':passed/len(DATASET),'cases':rows}
if __name__=='__main__': print(run_eval())
