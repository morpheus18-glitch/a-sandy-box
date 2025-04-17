import json
from pathlib import Path

def adjust_traits_live(agent_id, metrics, base_traits):
    """
    Dynamically shifts an agent's traits during simulation based on live metrics.
    """

    new_traits = base_traits.copy()

    dominance = metrics.get("dominance", 0)
    volatility = metrics.get("volatility", 0)
    intent_counts = metrics.get("intent_distribution", {})

    # Confidence is boosted by dominance
    if dominance > 0.3:
        new_traits["confidence"] = min(1.0, new_traits["confidence"] + 0.05)

    # Eloquence improves with diversity of intent
    if len(intent_counts) > 3:
        new_traits["eloquence"] = min(1.0, new_traits["eloquence"] + 0.03)

    # Strategic thinking drops slightly with high emotional volatility
    if volatility > 0.4:
        new_traits["strategic_thinking"] = max(0.3, new_traits["strategic_thinking"] - 0.02)

    # Leadership rises if multiple rounds had high intent counts
    total_intents = sum(intent_counts.values())
    if total_intents > 5 and intent_counts.get("challenge", 0) >= 2:
        new_traits["leadership"] += 0.02

    # Save updated memory (optional)
    update_memory(agent_id, new_traits)

    return new_traits

def update_memory(agent_id, traits):
    memory_path = Path(f"../../agents/memory/{agent_id}_memory.json")
    if not memory_path.exists():
        print(f"[TRAIT ADJUSTER] Warning: Memory file not found: {memory_path}")
        return

    with open(memory_path, 'r') as f:
        memory = json.load(f)

    memory["traits"].update(traits)
    with open(memory_path, 'w') as f:
        json.dump(memory, f, indent=2)

    print(f"[TRAIT ADJUSTER] Live traits updated for {agent_id}")