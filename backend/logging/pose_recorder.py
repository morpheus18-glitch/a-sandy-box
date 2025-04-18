import json
from pathlib import Path
from datetime import datetime

class PoseRecorder:
    def __init__(self, session_id, agent_id):
        self.session_id = session_id
        self.agent_id = agent_id
        self.buffer = []

    def record(self, enriched_msg):
        timestamp = datetime.utcnow().isoformat()
        entry = {
            "timestamp": timestamp,
            "message": enriched_msg.get("message", ""),
            "intent": enriched_msg.get("intent", ""),
            "tone": enriched_msg.get("tone", ""),
            "animation_state": enriched_msg.get("animation_state", {}),
            "expression_state": enriched_msg.get("expression_state", {})
        }
        self.buffer.append(entry)

    def save(self):
        path = Path(f"../../conversation/logs/{self.session_id}_{self.agent_id}.timeline")
        with open(path, 'w') as f:
            json.dump(self.buffer, f, indent=2)
        print(f"[RECORDER] Saved timeline: {path}")