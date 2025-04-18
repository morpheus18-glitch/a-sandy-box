import json
from pathlib import Path
from collections import defaultdict, Counter
import time

def analyze_conversation_log(log_path):
    with open(log_path, 'r') as f:
        lines = f.readlines()

    agents = set()
    intent_counter = defaultdict(Counter)
    rdip_flags = defaultdict(Counter)
    total_turns = 0
    leader_inference = Counter()

    for line in lines:
        msg = json.loads(line)
        speaker = msg.get("from_agent")
        agents.add(speaker)
        intent = msg.get("intent", "inform")
        confidence = msg.get("confidence", 0.5)

        intent_counter[speaker][intent] += 1
        total_turns += 1

        if "challenge" in intent or "question" in intent:
            rdip_flags[speaker]["epistemic_tension"] += 1
        if "agree" in intent or "negotiate" in intent:
            rdip_flags[speaker]["collaborative"] += 1
        if confidence > 0.9:
            rdip_flags[speaker]["dominant_tone"] += 1

        leader_inference[speaker] += confidence

    leader = leader_inference.most_common(1)[0][0]

    analysis = {
        "total_turns": total_turns,
        "dominant_intents": {a: dict(c) for a, c in intent_counter.items()},
        "rdip_flags": {a: dict(c) for a, c in rdip_flags.items()},
        "emergent_leader": leader
    }

    output_path = Path(log_path).with_suffix(".analysis")
    with open(output_path, 'w') as f:
        json.dump(analysis, f, indent=2)

    print(f"[ANALYZER] Analysis saved: {output_path.name}")
    return analysis