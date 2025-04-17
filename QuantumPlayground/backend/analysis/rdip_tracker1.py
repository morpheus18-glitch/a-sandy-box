import json
import numpy as np
from pathlib import Path
from collections import defaultdict

def track_rdip(session_id, agent_id):
    path = Path(f"../../conversation/logs/{session_id}_{agent_id}.timeline")
    if not path.exists():
        print(f"[RDIP] Timeline not found: {path}")
        return None

    with open(path, 'r') as f:
        timeline = json.load(f)

    total_turns = len(timeline)
    recursion_count = 0
    abstraction_score = 0
    contradiction_score = 0
    leadership_signals = 0
    self_reference = 0

    previous_responses = []

    for entry in timeline:
        msg = entry.get("message", "").lower()

        # Self-reference
        if any(phrase in msg for phrase in ["as i said", "i mentioned earlier", "remember when", "i already stated"]):
            recursion_count += 1
            self_reference += 1

        # Abstraction
        if any(phrase in msg for phrase in ["concept", "paradox", "perception", "framework", "recursive", "meta"]):
            abstraction_score += 1

        # Contradiction signal
        if any(phrase in msg for phrase in ["on the other hand", "but also", "however", "yet it seems"]):
            contradiction_score += 1

        # Leadership signals (assertion, persuasion)
        if any(phrase in msg for phrase in ["we must", "i propose", "let’s agree", "this is why"]):
            leadership_signals += 1

        # Recursive loop check
        if msg in previous_responses:
            recursion_count += 1
        previous_responses.append(msg)

    scores = {
        "rdip_score": round((recursion_count + abstraction_score + leadership_signals) / total_turns, 4),
        "recursive_refs": recursion_count,
        "self_reference": self_reference,
        "abstraction_hits": abstraction_score,
        "contradiction_hits": contradiction_score,
        "leadership_signals": leadership_signals,
        "turns_analyzed": total_turns
    }

    out_path = Path(f"../../agents/analysis/{agent_id}_rdip.json")
    with open(out_path, 'w') as f:
        json.dump(scores, f, indent=2)

    print(f"[RDIP] {agent_id} scored {scores['rdip_score']} | saved: {out_path}")
    return scores