import json
import random
from pathlib import Path

def evolve_abp(agent_id, session_id):
    path = Path(f"../../protocols/abp/{agent_id}.abp")
    if not path.exists():
        print(f"[ABP_EVOLVE] Missing ABP file: {path}")
        return

    with open(path, 'r') as f:
        abp = json.load(f)

    # Evolution logic:
    # If agent displayed strong emotional stability → reinforce current profile
    # If contradiction spikes or glitches detected → adjust feedback loop triggers

    metrics_path = Path(f"../../agents/analysis/{agent_id}_rdip.json")
    if not metrics_path.exists():
        print(f"[ABP_EVOLVE] Missing RDIP metrics for: {agent_id}")
        return

    with open(metrics_path, 'r') as f:
        rdip = json.load(f)

    # Mutation Conditions
    if rdip["volatility"] < 0.3:
        reinforce_behavior(abp, "confidence_high", weight=0.05)
    elif rdip["contradiction_hits"] > 3:
        mutate_feedback_loop(abp, "sync_loss", severity="increase")

    if rdip["leadership_signals"] > 5:
        reinforce_behavior(abp, "empathy_high", weight=0.03)

    # Save mutated ABP
    out_path = Path(f"../../protocols/abp/{agent_id}.abp")
    with open(out_path, 'w') as f:
        json.dump(abp, f, indent=2)

    print(f"[ABP_EVOLVE] {agent_id}'s ABP evolved based on RDIP + behavior analysis.")

def reinforce_behavior(abp, profile_key, weight=0.01):
    """Enhance gesture/pose weight for a given emotional profile."""
    if profile_key in abp["emotion_blend_profiles"]:
        profile = abp["emotion_blend_profiles"][profile_key]
        for k, v in profile.items():
            if isinstance(v, str): continue
            try:
                profile[k] = round(min(1.0, v + weight), 3)
            except:
                continue

def mutate_feedback_loop(abp, loop_key, severity="increase"):
    loop = abp["feedback_loops"].get(loop_key)
    if not loop: return

    if severity == "increase":
        loop["trigger"] = "contradiction_count > 2"
        loop["effect"] = "glitch_behavior"
        loop["override_voice"] = "distorted"
    elif severity == "decrease":
        loop["trigger"] = "contradiction_count > 5"