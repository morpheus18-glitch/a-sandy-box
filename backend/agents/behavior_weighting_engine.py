import json
from pathlib import Path
import math

def compute_behavior_weights(agent_id):
    """
    Generates a behavior profile dict with weighted intent probabilities and style parameters.
    """
    memory_path = Path(f"../../agents/memory/{agent_id}_memory.json")
    if not memory_path.exists():
        print(f"[BEHAVIOR] No memory file found for {agent_id}")
        return {}

    with open(memory_path, 'r') as f:
        memory = json.load(f)

    traits = memory.get("traits", {})
    rdip_log = extract_rdip_stats(memory.get("memory_log", []))

    weights = {
        "intent_bias": weighted_intent_distribution(traits, rdip_log),
        "tone_profile": determine_tone(traits),
        "response_style": response_pacing(traits)
    }

    return weights

def extract_rdip_stats(log):
    rdip = {
        "epistemic_tension": 0,
        "collaboration": 0,
        "dominant_tone": 0
    }
    for entry in log:
        summary = entry.get("summary", "").lower()
        if "challenge" in summary or "question" in summary:
            rdip["epistemic_tension"] += 1
        if "agree" in summary or "negotiate" in summary:
            rdip["collaboration"] += 1
        if "confidence" in summary:
            rdip["dominant_tone"] += 1
    return rdip

def weighted_intent_distribution(traits, rdip):
    """
    Dynamically adjusts intent selection probabilities.
    """
    base = {
        "inform": 1.0,
        "question": 1.0,
        "persuade": 1.0,
        "agree": 1.0,
        "challenge": 1.0,
        "deceive": 1.0
    }

    base["challenge"] += traits.get("confidence", 0.5) * 0.7
    base["agree"] += traits.get("empathy", 0.5) * 0.8
    base["persuade"] += traits.get("eloquence", 0.5) * 0.6
    base["question"] += (1.0 - traits.get("confidence", 0.5)) * 0.5

    base["deceive"] += max(0, (0.5 - traits.get("empathy", 0.5))) * 0.6

    # Normalize
    total = sum(base.values())
    return {k: v / total for k, v in base.items()}

def determine_tone(traits):
    if traits.get("leadership", 0) > 0.8:
        return "assertive"
    if traits.get("empathy", 0) > 0.8:
        return "soothing"
    return "neutral"

def response_pacing(traits):
    elo = traits.get("eloquence", 0.5)
    return "long-form" if elo > 0.7 else "brief"

# Example:
# weights = compute_behavior_weights("zenith")
# print(json.dumps(weights, indent=2))