import os
import json
import matplotlib.pyplot as plt
from pathlib import Path

def plot_trait_evolution(agent_id, sessions, output_dir="../../visuals/graphs/"):
    traits_over_time = {}

    for session in sessions:
        memory_path = Path(f"../../agents/snapshots/{session}/{agent_id}_memory.json")
        if not memory_path.exists():
            print(f"[GRAPHER] Missing: {memory_path}")
            continue

        with open(memory_path, 'r') as f:
            memory = json.load(f)

        for trait, value in memory.get("traits", {}).items():
            if trait not in traits_over_time:
                traits_over_time[trait] = []
            traits_over_time[trait].append(value)

    if not traits_over_time:
        print(f"[GRAPHER] No trait data found.")
        return

    plt.figure(figsize=(10, 6))
    for trait, values in traits_over_time.items():
        plt.plot(sessions[:len(values)], values, marker='o', label=trait)

    plt.title(f"Trait Evolution: {agent_id}")
    plt.xlabel("Session ID")
    plt.ylabel("Trait Value")
    plt.ylim(0, 1)
    plt.legend()
    plt.grid(True)

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    output_path = Path(output_dir) / f"{agent_id}_trait_evolution.png"
    plt.savefig(output_path)
    plt.close()

    print(f"[GRAPHER] Saved trait evolution graph: {output_path}")