import json
from pathlib import Path
import numpy as np

def run_trait_reinforcement(session_id, agent_id):
    path = Path(f"../../conversation/logs/{session_id}_{agent_id}.timeline")
    if not path.exists():
        print(f"[REINFORCEMENT] Timeline missing: {path}")
        return

    with open(path, 'r') as f:
        data = json.load(f)

    intents = [d.get("intent", "unknown") for d in data]
    sentiments = [d.get("sentiment", 0.0) for d in data]

    # Metrics
    diversity_score = len(set(intents)) / max(1, len(intents))
    avg_sentiment = np.mean(sentiments)
    volatility = np.std(sentiments)

    # Trait update logic
    delta = {
        "confidence": 0.01 if avg_sentiment > 0.3 else -0.01,
        "eloquence": 0.02 if diversity_score > 0.4 else -0.005,
        "leadership": 0.01 if "challenge" in intents else 0.0,
        "empathy": -0.01 if volatility > 0.5 else 0.01
    }

    _apply_trait_update(agent_id, delta)
    print(f"[REINFORCEMENT] Updated traits for {agent_id}: {delta}")

def _apply_trait_update(agent_id, delta):
    memory_path = Path(f"../../agents/memory/{agent_id}_memory.json")
    if not memory_path.exists():
        print(f"[REINFORCEMENT] Memory file missing: {memory_path}")
        return

    with open(memory_path, 'r') as f:
        memory = json.load(f)

    for trait, change in delta.items():
        current = memory["traits"].get(trait, 0.5)
        memory["traits"][trait] = round(min(1.0, max(0.0, current + change)), 3)

    with open(memory_path, 'w') as f:
        json.dump(memory, f, indent=2)