import json
from pathlib import Path
from collections import defaultdict
from backend.agents.trait_mutation_engine import clamp

def train_from_forked_arenas(parent_session_id, variation_ids):
    """
    Loads all forked arenas under a parent session and calculates global trait reinforcement
    based on repeated behavior across forks.
    """
    base_path = Path("../../conversation/logs/")
    summary = defaultdict(lambda: defaultdict(list))

    for vid in variation_ids:
        sid = f"{parent_session_id}_{vid}"
        analysis_path = base_path / f"{sid}.analysis"
        if not analysis_path.exists():
            print(f"[RECURSIVE] Missing: {sid}.analysis")
            continue

        with open(analysis_path, 'r') as f:
            analysis = json.load(f)

        for agent_id, intents in analysis.get("dominant_intents", {}).items():
            for intent, count in intents.items():
                summary[agent_id][intent].append(count)

    # Aggregate & reinforce traits
    for agent_id, intent_trend in summary.items():
        reinforcement = {
            "confidence": 0.0,
            "empathy": 0.0,
            "strategic_thinking": 0.0,
            "eloquence": 0.0
        }

        reinforce_map = {
            "persuade": "confidence",
            "agree": "empathy",
            "challenge": "strategic_thinking",
            "inform": "eloquence"
        }

        for intent, counts in intent_trend.items():
            avg = sum(counts) / len(counts)
            trait = reinforce_map.get(intent)
            if trait:
                reinforcement[trait] += 0.002 * avg  # subtle learning

        # Apply reinforcement
        mutate_traits_batch(agent_id, reinforcement)

def mutate_traits_batch(agent_id, trait_rewards):
    memory_path = Path(f"../../agents/memory/{agent_id}_memory.json")
    if not memory_path.exists():
        return

    with open(memory_path, 'r') as f:
        memory = json.load(f)

    traits = memory.get("traits", {})
    for k, delta in trait_rewards.items():
        if k in traits:
            traits[k] = clamp(traits[k] + delta)

    memory["traits"] = traits
    memory.setdefault("milestones", []).append(f"Recursive Training Boost: {list(trait_rewards.keys())}")
    with open(memory_path, 'w') as f:
        json.dump(memory, f, indent=2)

    print(f"[RECURSIVE] Updated {agent_id}: {trait_rewards}")