import json
from pathlib import Path
from collections import Counter
import numpy as np

def run_intent_sequence_learning(session_id, agent_id):
    path = Path(f"../../conversation/logs/{session_id}_{agent_id}.timeline")
    if not path.exists():
        print(f"[INTENT_LEARNER] Timeline missing: {path}")
        return

    with open(path, 'r') as f:
        timeline = json.load(f)

    intents = [entry.get("intent", "unknown") for entry in timeline]
    transitions = zip(intents[:-1], intents[1:])
    transition_counts = Counter(transitions)

    total = sum(transition_counts.values())
    transition_matrix = {f"{a}->{b}": round(c / total, 3) for (a, b), c in transition_counts.items()}

    output = {
        "agent_id": agent_id,
        "session": session_id,
        "total_turns": len(intents),
        "transition_matrix": transition_matrix
    }

    out_path = Path(f"../../agents/analysis/{agent_id}_intent_model.json")
    with open(out_path, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"[INTENT_LEARNER] Saved transition model to: {out_path}")