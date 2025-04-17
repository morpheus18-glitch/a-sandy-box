import json
from pathlib import Path

def stream_animation_output(agent_id, message_with_state):
    out_path = Path(f"../../unity_exports/{agent_id}_animation.json")
    with open(out_path, 'w') as f:
        json.dump(message_with_state, f, indent=2)
    print(f"[STREAM] {agent_id} animation state updated.")