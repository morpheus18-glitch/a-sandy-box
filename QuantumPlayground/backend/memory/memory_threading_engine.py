import json
from pathlib import Path
from glob import glob

def build_memory_thread(agent_id):
    """
    Scans all arena sessions, analysis logs, and memory logs to reconstruct an agent's
    narrative evolution and session-linked memory thread.
    """
    session_dir = Path("../../conversation/sessions/")
    memory_path = Path(f"../../agents/memory/{agent_id}_memory.json")

    if not memory_path.exists():
        print(f"[THREADING] Memory not found.")
        return

    with open(memory_path, 'r') as f:
        memory = json.load(f)

    sessions = []
    for file in session_dir.glob("*.arena"):
        with open(file, 'r') as f:
            data = json.load(f)
            if agent_id in data.get("agents", []):
                sessions.append({
                    "session_id": data["session_id"],
                    "prompt_id": data.get("prompt_id", "unknown"),
                    "rounds": data.get("rounds", 0),
                    "emergent_leader": get_leader(data["session_id"]),
                    "milestones": get_milestones(agent_id, data["session_id"])
                })

    memory["session_thread"] = sessions

    with open(memory_path, 'w') as f:
        json.dump(memory, f, indent=2)

    print(f"[THREADING] Memory thread built for {agent_id}. {len(sessions)} sessions linked.")

def get_leader(session_id):
    path = Path(f"../../conversation/logs/{session_id}.analysis")
    if not path.exists(): return None
    with open(path, 'r') as f:
        return json.load(f).get("emergent_leader")

def get_milestones(agent_id, session_id):
    log_path = Path(f"../../conversation/logs/{session_id}.traininglog")
    if not log_path.exists(): return []
    with open(log_path, 'r') as f:
        lines = f.readlines()
    return [f"Session:{session_id}:turn{ix}" for ix, line in enumerate(lines)
            if json.loads(line)["from_agent"] == agent_id]

# Example:
# build_memory_thread("aurora")