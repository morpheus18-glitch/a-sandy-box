import json
import datetime
from pathlib import Path

def update_agent_memory(agent_id, event_type, summary, protocol=None):
    memory_file = Path(f"../../agents/memory/{agent_id}_memory.json")

    if memory_file.exists():
        with open(memory_file, 'r') as f:
            memory = json.load(f)
    else:
        memory = {
            "agent_id": agent_id,
            "created_at": datetime.datetime.utcnow().isoformat(),
            "memory_log": [],
            "traits": {
                "empathy": 0.5,
                "strategic_thinking": 0.5,
                "eloquence": 0.5,
                "confidence": 0.5,
                "leadership": 0.5
            },
            "milestones": []
        }

    memory["memory_log"].append({
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "event_type": event_type,
        "summary": summary,
        "linked_protocol": protocol
    })

    with open(memory_file, 'w') as f:
        json.dump(memory, f, indent=2)

    print(f"[MEMORY] Logged event for {agent_id}: {summary}")