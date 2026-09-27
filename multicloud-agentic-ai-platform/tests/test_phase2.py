from agents.graph import build_graph
from a2a.service import A2ATask, handle_task, agent_card
from agents.core import Supervisor

def test_graph():
    out=build_graph().invoke({'question':'Review Azure private endpoint security'})
    assert out['result']['blocked'] is False

def test_a2a():
    s=Supervisor(); r=handle_task(A2ATask(task_id='t1',message='Review AWS IAM security'),s)
    assert r['status']=='completed' and r['task_id']=='t1'

def test_card(): assert 'rag' in agent_card()['capabilities']
