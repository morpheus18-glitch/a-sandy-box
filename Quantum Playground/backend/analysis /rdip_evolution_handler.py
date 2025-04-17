import json
from pathlib import Path

def evolve_agent_by_rdip(agent_id):
    path = Path(f"../../agents/analysis/{agent_id}_rdip.json")
    memory_path = Path(f"../../agents/memory/{agent_id}_memory.json")

    if not path.exists() or not memory_path.exists():
        print(f"[RDIP_EVOLVE] Missing RDIP or memory file.")
        return

    with open(path, 'r') as f:
        rdip = json.load(f)

    with open(memory_path, 'r') as f:
        memory = json.load(f)

    current_tags = memory.get("milestones", [])
    tier = memory.get("tier", 1)

    # Evolution logic
    if rdip["rdip_score"] > 0.5 and "recursive_thinker" not in current_tags:
        current_tags.append("recursive_thinker")
        tier += 1

    if rdip["abstraction_hits"] > 5 and "abstractor" not in current_tags:
        current_tags.append("abstractor")

    if rdip["leadership_signals"] > 3:
        memory["traits"]["leadership"] = min(1.0, memory["traits"].get("leadership", 0.5) + 0.05)

    memory["milestones"] = current_tags
    memory["tier"] = tier

    with open(memory_path, 'w') as f:
        json.dump(memory, f, indent=2)

    print(f"[RDIP_EVOLVE] {agent_id} evolved to tier {tier} with milestones: {current_tags}")