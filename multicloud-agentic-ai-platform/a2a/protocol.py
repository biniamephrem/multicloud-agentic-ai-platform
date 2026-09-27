from pydantic import BaseModel
class A2AMessage(BaseModel):
    sender:str; recipient:str; task:str; correlation_id:str
class A2AResponse(BaseModel):
    correlation_id:str; status:str; result:str
def send(message:A2AMessage):
    return A2AResponse(correlation_id=message.correlation_id,status='completed',result=f'{message.recipient} completed delegated task: {message.task}')
