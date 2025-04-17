import json
from pathlib import Path

def promote_agent_if_eligible(agent_id):
    memory_path = Path(f"../../agents/memory/{agent_id}_memory.json")
    if not memory_path.exists():
        print(f"[PROMOTION] Memory not found for {agent_id}")
        return None

    with open(memory_path, 'r') as f:
        memory = json.load(f)

    traits = memory.get("traits", {})
    current_milestones = set(memory.get("milestones", []))

    promotions = []

    # Promotion Logic
    if traits.get("leadership", 0) > 0.85 and "Promoted: Leader" not in current_milestones:
        promotions.append("Promoted: Leader")
        memory["milestones"].append("Promoted: Leader")

    if traits.get("empathy", 0) > 0.9 and traits.get("eloquence", 0) > 0.7 and "Ascended: Diplomat" not in current_milestones:
        promotions.append("Ascended: Diplomat")
        memory["milestones"].append("Ascended: Diplomat")

    if traits.get("strategic_thinking", 0) > 0.9 and "Evolved: Tactical Mind" not in current_milestones:
        promotions.append("Evolved: Tactical Mind")
        memory["milestones"].append("Evolved: Tactical Mind")

    if not promotions:
        print(f"[PROMOTION] No promotions earned.")
        return None

    # Optional: auto-broadcast or trigger external effects
    memory["traits"] = apply_promotion_bonuses(traits, promotions)
    with open(memory_path, 'w') as f:
        json.dump(memory, f, indent=2)

    print(f"[PROMOTION] {agent_id} received: {promotions}")
    return promotions

def apply_promotion_bonuses(traits, promotions):
    """
    Add tiny bonuses or unlocks based on promotions (optional).
    """
    for promo in promotions:
        if "Leader" in promo:
            traits["confidence"] = min(1.0, traits.get("confidence", 0.5) + 0.05)
        if "Diplomat" in promo:
            traits["empathy"] = min(1.0, traits.get("empathy", 0.5) + 0.05)
        if "Tactical" in promo:
            traits["strategic_thinking"] = min(1.0, traits.get("strategic_thinking", 0.5) + 0.04)
    return traits

# Example:
# promote_agent_if_eligible("zenith")