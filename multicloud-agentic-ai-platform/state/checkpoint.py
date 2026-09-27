"""Persistent conversation/checkpoint store with SQLite fallback."""
import json, sqlite3
from pathlib import Path

class CheckpointStore:
    def __init__(self, path: str = "data/checkpoints.db"):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(path, check_same_thread=False)
        self.db.execute("CREATE TABLE IF NOT EXISTS checkpoints (thread_id TEXT PRIMARY KEY, payload TEXT NOT NULL)")
    def put(self, thread_id: str, payload: dict):
        self.db.execute("INSERT OR REPLACE INTO checkpoints VALUES (?,?)", (thread_id, json.dumps(payload)))
        self.db.commit()
    def get(self, thread_id: str):
        row = self.db.execute("SELECT payload FROM checkpoints WHERE thread_id=?", (thread_id,)).fetchone()
        return json.loads(row[0]) if row else None
