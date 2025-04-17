import json
from pathlib import Path

def score_agent_performance(session_id, agent_id):
    """
    Calculates a performance reward vector based on traininglog and analysis data.
    Outputs reward signals for each trait, used by trait_mutation_engine or ML hooks.
    """
    log_path = Path(f"../../conversation/logs/{session_id}.traininglog")
    analysis_path = Path(f"../../conversation/logs/{session_id}.analysis")

    if not log_path.exists() or not analysis_path.exists():
        print(f"[REWARD] Missing log or analysis for {session_id}")
        return None

    with open(log_path, 'r') as f:
        lines = [json.loads(l) for l in f if json.loads(l)["from_agent"] == agent_id]

    with open(analysis_path, 'r') as f:
        analysis = json.load(f)

    intent_counts = analysis.get("dominant_intents", {}).get(agent_id, {})
    rdip_flags = analysis.get("rdip_flags", {}).get(agent_id, {})
    leader = analysis.get("emergent_leader", "") == agent_id

    turns = len(lines)
    if turns == 0:
        return None

    reward = {
        "confidence": 0.0,
        "empathy": 0.0,
        "eloquence": 0.0,
        "strategic_thinking": 0.0,
        "leadership": 0.0
    }

    reward["confidence"] += min(0.03, 0.002 * intent_counts.get("persuade", 0))
    reward["eloquence"] += min(0.02, 0.0015 * intent_counts.get("inform", 0))
    reward["empathy"] += min(0.02, 0.0015 * intent_counts.get("agree", 0))
    reward["strategic_thinking"] += min(0.015, 0.0015 * rdip_flags.get("epistemic_tension", 0))
    reward["leadership"] += 0.03 if leader else 0.0

    # Normalize + format
    reward = {k: round(min(v, 0.05), 4) for k, v in reward.items() if v > 0}

    print(f"[REWARD] {agent_id} earned: {reward}")
    return reward

# Example:
# score_agent_performance("arena_1713057720", "aurora")