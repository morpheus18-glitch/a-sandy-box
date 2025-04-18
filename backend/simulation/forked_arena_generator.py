import json
import shutil
from pathlib import Path
from datetime import datetime
from backend.agents.agent_cloner import clone_agent

def fork_arena(session_id, variation_id="v2", clone_agents=True, prompt_override=None):
    """
    Forks an arena by creating a new session file with cloned agents and optional prompt changes.
    """
    base_path = Path("../../conversation/sessions/")
    arena_path = base_path / f"{session_id}.arena"

    if not arena_path.exists():
        print(f"[FORK] Original arena not found: {session_id}")
        return None

    with open(arena_path, 'r') as f:
        arena = json.load(f)

    new_agents = []
    for a in arena["agents"]:
        clone_id = clone_agent(a, mutate=True) if clone_agents else a
        new_agents.append(clone_id)

    new_prompt = prompt_override or arena.get("prompt_id")
    new_session_id = f"{session_id}_{variation_id}"

    forked_arena = {
        "session_id": new_session_id,
        "prompt_id": new_prompt,
        "agents": new_agents,
        "rounds": arena["rounds"],
        "start_time": datetime.utcnow().isoformat(),
        "parent_session": session_id,
        "variation_id": variation_id
    }

    new_path = base_path / f"{new_session_id}.arena"
    with open(new_path, 'w') as f:
        json.dump(forked_arena, f, indent=2)

    print(f"[FORK] Forked arena created: {new_session_id}")
    return new_session_id

# Example:
# fork_arena("arena_1713057720", variation_id="v3", clone_agents=True)