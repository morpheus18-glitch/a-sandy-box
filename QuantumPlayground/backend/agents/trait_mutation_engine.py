import json
import random
from pathlib import Path

def mutate_agent_traits(agent_id, behavior_summary):
    """
    Applies micro-adjustments to agent traits based on observed behavioral outcomes.
    """
    memory_path = Path(f"../../agents/memory/{agent_id}_memory.json")
    if not memory_path.exists():
        print(f"[MUTATION] Memory file not found.")
        return

    with open(memory_path, 'r') as f:
        memory = json.load(f)

    traits = memory.get("traits", {})
    summary = behavior_summary.lower()

    if "dominated" in summary:
        traits["confidence"] = clamp(traits.get("confidence", 0.5) + 0.02)
        traits["leadership"] = clamp(traits.get("leadership", 0.5) + 0.01)

    if "agreed" in summary or "aligned":
        traits["empathy"] = clamp(traits.get("empathy", 0.5) + 0.015)

    if "challenged" in summary:
        traits["strategic_thinking"] = clamp(traits.get("strategic_thinking", 0.5) + 0.01)

    if "conflicted" in summary:
        traits["confidence"] = clamp(traits.get("confidence", 0.5) - 0.015)

    # ML Reinforcement Integration (hook-ready)
    traits = ml_reward_hook(agent_id, traits)

    memory["traits"] = traits
    with open(memory_path, 'w') as f:
        json.dump(memory, f, indent=2)

    print(f"[MUTATION] Traits updated for {agent_id}")

def clamp(value, min_val=0.0, max_val=1.0):
    return max(min_val, min(max_val, round(value, 3)))

def ml_reward_hook(agent_id, traits):
    """
    Custom ML algorithm reward signal placeholder.
    You can plug in reinforcement learning feedback here.
    """
    # Example: if model scored +0.03 reward for 'confidence'
    if agent_id == "aurora":
        traits["confidence"] = clamp(traits["confidence"] + 0.03)
    return traits

# Example:
# mutate_agent_traits("aurora", "aurora dominated the dialogue with persuasive confidence.")