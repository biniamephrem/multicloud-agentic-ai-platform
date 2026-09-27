from fastapi import FastAPI
from pydantic import BaseModel
from agents.core import Supervisor
from agents.graph import build_graph
from mcp_server.server import list_tools,call_tool
from evaluation.eval import run_eval
from a2a.service import A2ATask,agent_card,handle_task
app=FastAPI(title='Multi-Cloud Agentic AI Platform',version='2.0.0'); supervisor=Supervisor(); graph=build_graph(supervisor)
class Ask(BaseModel): question:str
class ToolCall(BaseModel): name:str; args:dict={}; approved:bool=False
@app.get('/health')
def health(): return {'status':'ok','version':'2.0.0'}
@app.post('/ask')
def ask(req:Ask): return graph.invoke({'question':req.question})['result']
@app.get('/mcp/tools')
def tools(): return list_tools()
@app.post('/mcp/call')
def tool(req:ToolCall): return call_tool(req.name,req.args,req.approved)
@app.get('/a2a/agent-card')
def card(): return agent_card()
@app.post('/a2a/tasks')
def a2a_task(req:A2ATask): return handle_task(req,supervisor)
@app.get('/eval')
def eval_endpoint(): return run_eval()
