import json
from pathlib import Path
import numpy as np

def run_memory_embedding(session_id, agent_id):
    memory_path = Path(f"../../conversation/logs/{session_id}_{agent_id}.timeline")
    if not memory_path.exists():
        print(f"[EMBEDDING] Timeline not found: {memory_path}")
        return

    with open(memory_path, 'r') as f:
        timeline = json.load(f)

    sentiments = [entry.get("sentiment", 0.0) for entry in timeline]
    intent_counts = {}
    for entry in timeline:
        intent = entry.get("intent", "unknown")
        intent_counts[intent] = intent_counts.get(intent, 0) + 1

    embedding = [
        round(np.mean(sentiments), 4),
        round(np.std(sentiments), 4),
        intent_counts.get("inform", 0),
        intent_counts.get("challenge", 0),
        intent_counts.get("agree", 0),
        intent_counts.get("deceive", 0)
    ]

    out_path = Path(f"../../agents/embeddings/{agent_id}_embedding.json")
    with open(out_path, 'w') as f:
        json.dump({"vector": embedding, "traits": intent_counts}, f, indent=2)

    print(f"[EMBEDDING] Memory embedding vector saved for {agent_id}: {embedding}")