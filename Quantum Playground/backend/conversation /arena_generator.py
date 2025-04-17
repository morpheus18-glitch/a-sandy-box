import json
import time
from pathlib import Path

def generate_arena_metadata(agent_ids, prompt_id, rounds):
    metadata = {
        "session_id": f"arena_{int(time.time())}",
        "agents": agent_ids,
        "prompt_id": prompt_id,
        "start_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "rounds": rounds,
        "topics_emerged": [],
        "dominant_intents": {},
        "emergent_leader": None,
        "conflict_points": [],
        "rdip_score": {},
        "training_log_ref": None
    }

    arena_path = Path(f"../../conversation/sessions/{metadata['session_id']}.arena")
    with open(arena_path, 'w') as f:
        json.dump(metadata, f, indent=2)

    print(f"[ARENA GEN] Metadata saved: {arena_path.name}")
    return metadata