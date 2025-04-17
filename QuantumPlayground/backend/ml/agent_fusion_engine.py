import json
from pathlib import Path
import random

def fuse_agents(agent_id_1, agent_id_2, session_id):
    e1 = load_embedding(agent_id_1)
    e2 = load_embedding(agent_id_2)

    if not e1 or not e2:
        print("[FUSION] Missing embeddings. Abort.")
        return None

    fused_id = f"fusion_{agent_id_1}_{agent_id_2}_{random.randint(1000,9999)}"

    fused_vector = [(a + b) / 2 for a, b in zip(e1["vector"], e2["vector"])]
    fused_traits = {k: round((e1["traits"].get(k, 0) + e2["traits"].get(k, 0)) / 2, 3)
                    for k in set(e1["traits"]) | set(e2["traits"])}

    fused_identity = {
        "agent_id": fused_id,
        "parents": [agent_id_1, agent_id_2],
        "created_from_session": session_id,
        "vector": [round(v, 4) for v in fused_vector],
        "traits": fused_traits,
        "notes": "Fused via AFTF: Agent Fusion via Trait Folding"
    }

    out_path = Path(f"../../agents/fused/{fused_id}_fused.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w') as f:
        json.dump(fused_identity, f, indent=2)

    print(f"[FUSION] Agent fusion complete: {fused_id}")
    return fused_id

def load_embedding(agent_id):
    path = Path(f"../../agents/embeddings/{agent_id}_embedding.json")
    if not path.exists():
        return None
    with open(path, 'r') as f:
        return json.load(f)