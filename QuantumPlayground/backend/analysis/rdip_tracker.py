import json
from pathlib import Path
from collections import defaultdict
from textblob import TextBlob

LOG_PATH = Path("../../conversation/logs/")
OUTPUT_PATH = Path("../../rdip/")

def analyze_session(session_id, agents):
    results = {}

    for agent_id in agents:
        timeline_file = LOG_PATH / f"{session_id}_{agent_id}.timeline"
        if not timeline_file.exists():
            continue

        with open(timeline_file, 'r') as f:
            timeline = json.load(f)

        rdip_data = {
            "agent_id": agent_id,
            "recursive_mentions": 0,
            "self_reference": 0,
            "meta_cognition": 0,
            "leadership_signals": 0,
            "avg_sentiment": 0.0,
            "recursion_depth_score": 0.0
        }

        sentiments = []
        for entry in timeline:
            msg = entry["message"].lower()
            sentiments.append(entry.get("sentiment", 0.0))

            if "as i said" in msg or "previously mentioned" in msg:
                rdip_data["recursive_mentions"] += 1

            if "i think" in msg or "i believe" in msg:
                rdip_data["self_reference"] += 1

            if "i’m aware that" in msg or "i know i’m saying" in msg:
                rdip_data["meta_cognition"] += 1

            if "let me guide this" in msg or "i’ll lead" in msg:
                rdip_data["leadership_signals"] += 1

        total_turns = len(timeline)
        rdip_data["avg_sentiment"] = round(sum(sentiments) / total_turns, 3) if total_turns else 0.0

        # Composite recursion score (can be refined with ML later)
        rdip_data["recursion_depth_score"] = round(
            0.4 * rdip_data["recursive_mentions"] +
            0.3 * rdip_data["meta_cognition"] +
            0.3 * rdip_data["self_reference"],
            2
        )

        results[agent_id] = rdip_data

        # Save per-agent analysis
        OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
        path = OUTPUT_PATH / f"{session_id}_{agent_id}_rdip.json"
        with open(path, 'w') as f:
            json.dump(rdip_data, f, indent=2)

        print(f"[RDiP] Analysis complete for {agent_id} — Score: {rdip_data['recursion_depth_score']}")

    return results