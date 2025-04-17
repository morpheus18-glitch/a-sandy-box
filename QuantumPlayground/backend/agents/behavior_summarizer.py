import json
from collections import Counter
from pathlib import Path

def summarize_behavior_from_log(session_id, agent_id):
    """
    Analyzes a `.traininglog` and summarizes how the agent behaved.
    Returns a natural-language string + stats object.
    """
    log_path = Path(f"../../conversation/logs/{session_id}.traininglog")
    if not log_path.exists():
        print(f"[SUMMARY] Training log not found for {session_id}")
        return None, None

    with open(log_path, 'r') as f:
        lines = f.readlines()

    intent_counter = Counter()
    turn_count = 0
    avg_conf = 0.0
    max_conf = 0.0

    for line in lines:
        msg = json.loads(line)
        if msg.get("from_agent") != agent_id:
            continue
        intent = msg.get("intent", "inform")
        intent_counter[intent] += 1
        conf = msg.get("confidence", 0.5)
        avg_conf += conf
        max_conf = max(max_conf, conf)
        turn_count += 1

    if turn_count == 0:
        return "No behavior recorded.", {}

    avg_conf /= turn_count

    description = generate_narrative(intent_counter, avg_conf, max_conf, turn_count)

    stats = {
        "turns": turn_count,
        "intent_counts": dict(intent_counter),
        "avg_conf": round(avg_conf, 3),
        "max_conf": round(max_conf, 3)
    }

    return description, stats

def generate_narrative(intents, avg_conf, max_conf, turns):
    leaderish = avg_conf > 0.85 and intents.get("persuade", 0) + intents.get("inform", 0) > intents.get("question", 0)

    if leaderish:
        return "Dominated the conversation with confident persuasion and clear directives."

    if intents.get("question", 0) > turns * 0.4:
        return "Adopted a curious and exploratory tone, often challenging or probing ideas."

    if intents.get("agree", 0) > turns * 0.3:
        return "Aligned with other agents, showing signs of collaboration and consensus building."

    if intents.get("deceive", 0) > 0:
        return "Exhibited deceptive or misdirecting behavior during key exchanges."

    return "Maintained a balanced conversational style with mixed intents and adaptive responses."

# Example:
# desc, stats = summarize_behavior_from_log("arena_1713057720", "zenith")
# print(desc); print(stats)