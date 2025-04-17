import json
import os
from pathlib import Path
from glob import glob

def load_agent_memory(agent_id):
    memory_path = Path(f"../../agents/memory/{agent_id}_memory.json")
    if not memory_path.exists():
        print(f"[DASHBOARD] No memory file for {agent_id}")
        return None

    with open(memory_path, 'r') as f:
        return json.load(f)

def list_training_sessions(agent_id):
    session_dir = Path("../../conversation/sessions/")
    matching_sessions = []

    for file in session_dir.glob("*.arena"):
        with open(file, 'r') as f:
            data = json.load(f)
            if agent_id in data.get("agents", []):
                matching_sessions.append({
                    "session_id": data["session_id"],
                    "prompt_id": data["prompt_id"],
                    "rounds": data["rounds"],
                    "leader": get_leader_from_analysis(data["session_id"])
                })

    return matching_sessions

def get_leader_from_analysis(session_id):
    analysis_path = Path(f"../../conversation/logs/{session_id}.analysis")
    if not analysis_path.exists():
        return None
    with open(analysis_path, 'r') as f:
        data = json.load(f)
    return data.get("emergent_leader")

def display_dashboard(agent_id):
    memory = load_agent_memory(agent_id)
    if not memory:
        return

    print(f"\n===== AGENT DASHBOARD: {agent_id.upper()} =====")
    print(f"Created At : {memory['created_at']}")
    print(f"Traits     :")
    for k, v in memory["traits"].items():
        print(f"  - {k}: {v:.2f}")

    print("\nMilestones :")
    for m in memory.get("milestones", []):
        print(f"  * {m}")

    print("\nRecent Sessions:")
    sessions = list_training_sessions(agent_id)
    for s in sessions[-5:]:
        leader_flag = "(LEADER)" if s["leader"] == agent_id else ""
        print(f"  - {s['session_id']} ({s['prompt_id']}) Rounds: {s['rounds']} {leader_flag}")

    print("\nLog complete.\n")

# Example usage:
# display_dashboard("aurora")