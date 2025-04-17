import json
import random
import numpy as np
from pathlib import Path
from copy import deepcopy

def run_nesi_swarm(agent_ids, session_id, num_generations=5, selection_rate=0.4, mutation_rate=0.1):
    print(f"\n[NESI] Starting swarm evolution: session={session_id}, agents={agent_ids}")

    agents = [load_embedding(agent_id) for agent_id in agent_ids]
    for generation in range(num_generations):
        print(f"\n[NESI] Generation {generation + 1}")
        scored_agents = score_population(agents)
        elites = select_elite(scored_agents, rate=selection_rate)

        new_agents = crossover_and_mutate(elites, mutation_rate)
        agents = elites + new_agents

    save_final_population(agents, session_id)
    print(f"\n[NESI] Final swarm saved for session: {session_id}")

# === Helpers ===

def load_embedding(agent_id):
    path = Path(f"../../agents/embeddings/{agent_id}_embedding.json")
    if not path.exists():
        print(f"[NESI] Missing embedding: {agent_id}")
        return {"agent_id": agent_id, "vector": [0.0]*6, "traits": {}}
    with open(path, 'r') as f:
        data = json.load(f)
    data["agent_id"] = agent_id
    return data

def score_population(agents):
    for a in agents:
        vec = a["vector"]
        # Example: score = avg sentiment + diversity weight - volatility
        a["score"] = vec[0] + 0.1 * sum(vec[2:]) - 0.5 * vec[1]
    return sorted(agents, key=lambda x: x["score"], reverse=True)

def select_elite(agents, rate=0.4):
    cutoff = max(2, int(len(agents) * rate))
    return deepcopy(agents[:cutoff])

def crossover_and_mutate(parents, mutation_rate):
    new_gen = []
    for _ in range(len(parents)):
        p1, p2 = random.sample(parents, 2)
        child_vec = [(a + b) / 2 for a, b in zip(p1["vector"], p2["vector"])]
        # Mutate
        for i in range(len(child_vec)):
            if random.random() < mutation_rate:
                child_vec[i] += random.uniform(-0.1, 0.1)

        child = {
            "agent_id": f"nesi_{p1['agent_id']}_{p2['agent_id']}_{random.randint(1000,9999)}",
            "vector": [round(v, 4) for v in child_vec],
            "traits": merge_traits(p1["traits"], p2["traits"])
        }
        new_gen.append(child)
    return new_gen

def merge_traits(t1, t2):
    keys = set(t1.keys()) | set(t2.keys())
    return {k: (t1.get(k, 0) + t2.get(k, 0)) // 2 for k in keys}

def save_final_population(population, session_id):
    out_dir = Path(f"../../agents/nesi_results/{session_id}/")
    out_dir.mkdir(parents=True, exist_ok=True)
    for agent in population:
        path = out_dir / f"{agent['agent_id']}_nesi.json"
        with open(path, 'w') as f:
            json.dump(agent, f, indent=2)