import json
import random
import shutil
from pathlib import Path
from datetime import datetime

def clone_agent(agent_id, clone_name=None, mutate=True):
    """
    Creates a copy of the given agent with a new ID.
    Optionally applies slight mutations to traits.
    """
    source_path = Path(f"../../agents/memory/{agent_id}_memory.json")
    if not source_path.exists():
        print(f"[CLONE] Source agent not found: {agent_id}")
        return None

    with open(source_path, 'r') as f:
        memory = json.load(f)

    clone_id = clone_name or f"{agent_id}_v{random.randint(1000,9999)}"
    clone_path = Path(f"../../agents/memory/{clone_id}_memory.json")

    # Mutate traits slightly if enabled
    traits = memory.get("traits", {})
    if mutate:
        traits = {k: clamp(v + random.gauss(0, 0.01)) for k, v in traits.items()}

    clone_memory = {
        "agent_id": clone_id,
        "created_at": datetime.utcnow().isoformat(),
        "traits": traits,
        "memory_log": [],
        "milestones": ["Cloned from: " + agent_id],
        "lineage": {
            "parent": agent_id,
            "genesis": memory.get("created_at"),
            "descendants": []
        }
    }

    # Update parent lineage
    memory.setdefault("lineage", {}).setdefault("descendants", []).append(clone_id)
    with open(source_path, 'w') as f:
        json.dump(memory, f, indent=2)

    # Save clone
    with open(clone_path, 'w') as f:
        json.dump(clone_memory, f, indent=2)

    print(f"[CLONE] Created agent clone: {clone_id}")
    return clone_id

def clamp(v, lo=0.0, hi=1.0):
    return round(max(lo, min(hi, v)), 3)

# Example:
# clone_agent("aurora", mutate=True)