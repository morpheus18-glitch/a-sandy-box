import json
import time
from pathlib import Path

class TrainingLogger:
    def __init__(self, session_id):
        """
        Initializes a training logger with a specific session ID.
        All conversation turns and commentary will be saved as JSONL.
        """
        self.session_id = session_id
        self.log_path = Path(f"../../conversation/logs/{session_id}.traininglog")
        self.turn_id = 0

    def log_turn(self, message_dict):
        """
        Logs a single conversation turn.
        message_dict should include:
        - from_agent
        - to_agent (optional)
        - message
        - intent
        - confidence
        """
        message_dict["turn_id"] = self.turn_id
        self.turn_id += 1
        message_dict["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        with open(self.log_path, 'a') as f:
            f.write(json.dumps(message_dict) + "\n")

    def log_commentary(self, agent_id, comment):
        """
        Logs a meta-commentary message (not part of main dialogue loop).
        Useful for agent reflections or injected user evaluations.
        """
        self.log_turn({
            "from_agent": agent_id,
            "message": comment,
            "intent": "meta_comment",
            "confidence": 1.0
        })

    def get_log_path(self):
        return str(self.log_path)

    def summarize_log(self):
        """
        Returns basic metadata from the log.
        Can be expanded to feed into live dashboards.
        """
        if not self.log_path.exists():
            return None

        with open(self.log_path, 'r') as f:
            lines = f.readlines()

        return {
            "session_id": self.session_id,
            "total_turns": len(lines),
            "agents_involved": list(set(json.loads(line)["from_agent"] for line in lines))
        }