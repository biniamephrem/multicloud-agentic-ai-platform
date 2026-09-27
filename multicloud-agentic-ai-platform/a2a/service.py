from pydantic import BaseModel
class AgentCard(BaseModel):
    name:str="multicloud-ops-agent"; version:str="2.0"; capabilities:list[str]=["rag","cloud-ops","security","terraform"]
class A2ATask(BaseModel):
    task_id:str; message:str; context:dict={}
def agent_card(): return AgentCard().model_dump()
def handle_task(task:A2ATask, supervisor):
    return {"task_id":task.task_id,"status":"completed","result":supervisor.route(task.message)}
