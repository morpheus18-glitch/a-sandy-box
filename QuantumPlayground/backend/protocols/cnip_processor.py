import json
import numpy as np
from collections import defaultdict
from pathlib import Path

def load_cnip(agent_id):
    path = Path(f"../../protocols/cnip/{agent_id}.cnip")
    if not path.exists():
        print(f"[CNIP] Missing protocol file: {path}")
        return default_cnip()
    with open(path, 'r') as f:
        return json.load(f)

def default_cnip():
    return {
        "max_focus_targets": 2,
        "tone_weights": {
            "neutral": 1.0,
            "emotional": 1.2,
            "aggressive": 1.5,
            "supportive": 0.8
        },
        "proximity_bias": 1.0,
        "interrupt_penalty": 0.6,
        "acknowledgment_threshold": 0.4
    }

def process_crowd_input(agent_id, incoming_messages, agent_focus=None):
    """
    incoming_messages: list of dicts like:
    [
        {"from": "orion", "message": "...", "tone": "aggressive", "intent": "challenge", "priority": 0.7},
        {"from": "aurora", "message": "...", "tone": "supportive", "intent": "inform", "priority": 0.3}
    ]
    """

    cnip = load_cnip(agent_id)
    scores = {}

    for msg in incoming_messages:
        tone_weight = cnip["tone_weights"].get(msg.get("tone", "neutral"), 1.0)
        base_score = msg.get("priority", 0.5) * tone_weight

        if agent_focus and msg["from"] == agent_focus:
            base_score *= 1.25

        scores[msg["from"]] = round(base_score, 3)

    # Normalize + sort
    if not scores:
        return {"primary": None, "acknowledge": []}

    sorted_agents = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    primary = sorted_agents[0][0]
    acknowledgments = [a for a, score in sorted_agents[1:]
                       if score > cnip["acknowledgment_threshold"]]

    return {
        "primary": primary,
        "acknowledge": acknowledgments,
        "weights": scores
    }

# Example:
# agent_id = "zenith"
# msgs = [{"from": "orion", "tone": "aggressive", "priority": 0.8},
#         {"from": "aurora", "tone": "supportive", "priority": 0.3}]
# result = process_crowd_input(agent_id, msgs)
# → {'primary': 'orion', 'acknowledge': ['aurora'], 'weights': {...}}