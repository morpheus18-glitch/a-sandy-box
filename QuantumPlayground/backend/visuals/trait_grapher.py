import json
import matplotlib.pyplot as plt
from pathlib import Path

def plot_trait_evolution(agent_id):
    memory_path = Path(f"../../agents/memory/{agent_id}_memory.json")
    if not memory_path.exists():
        print(f"[GRAPHER] No memory for {agent_id}")
        return

    with open(memory_path, 'r') as f:
        memory = json.load(f)

    traits = memory.get("traits", {})
    log = memory.get("memory_log", [])
    timeline = [entry["timestamp"] for entry in log if entry["event_type"] == "Training Session"]
    updates = []

    for t in timeline:
        updates.append(dict(traits))  # assumes traits are updated incrementally

    if not updates:
        print(f"[GRAPHER] No evolution data to plot.")
        return

    trait_keys = list(traits.keys())
    for trait in trait_keys:
        values = [update.get(trait, 0.5) for update in updates]
        plt.plot(range(len(values)), values, label=trait)

    plt.title(f"Trait Evolution: {agent_id}")
    plt.xlabel("Training Events")
    plt.ylabel("Trait Value")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Example:
# plot_trait_evolution("aurora")