from typing import TypedDict
from agents.core import Supervisor
class AgentState(TypedDict, total=False):
    question:str; result:dict

def build_graph(supervisor:Supervisor|None=None):
    """LangGraph orchestration with a safe fallback when optional dependency is absent."""
    sup=supervisor or Supervisor()
    try:
        from langgraph.graph import StateGraph, START, END
        def orchestrate(state:AgentState): return {"result":sup.route(state["question"])}
        g=StateGraph(AgentState); g.add_node("orchestrate",orchestrate); g.add_edge(START,"orchestrate"); g.add_edge("orchestrate",END)
        return g.compile()
    except ImportError:
        class Fallback:
            def invoke(self,state): return {**state,"result":sup.route(state["question"])}
        return Fallback()
