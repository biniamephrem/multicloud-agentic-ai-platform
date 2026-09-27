import time, uuid
from contextlib import contextmanager
@contextmanager
def trace(name:str, attrs:dict|None=None):
    started=time.perf_counter(); trace_id=str(uuid.uuid4())
    record={"trace_id":trace_id,"span":name,"attrs":attrs or {}}
    try: yield record
    finally: record["latency_ms"]=round((time.perf_counter()-started)*1000,2)
