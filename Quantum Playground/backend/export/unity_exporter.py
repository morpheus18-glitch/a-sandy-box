import json
from pathlib import Path

def export_unity_timeline(session_id, agent_id):
    log_path = Path(f"../../conversation/logs/{session_id}.traininglog")
    output_path = Path(f"../../unity_exports/{agent_id}_{session_id}.unitytimeline")

    if not log_path.exists():
        print("[UNITY] Log file not found.")
        return

    timeline = []
    with open(log_path, 'r') as f:
        for line in f:
            msg = json.loads(line)
            if msg["from_agent"] != agent_id:
                continue
            entry = {
                "timestamp": msg.get("timestamp"),
                "text": msg.get("message"),
                "gesture": infer_gesture(msg["intent"]),
                "emotion": infer_emotion(msg["intent"], msg.get("confidence", 0.5))
            }
            timeline.append(entry)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(timeline, f, indent=2)

    print(f"[UNITY] Export complete: {output_path.name}")

def infer_gesture(intent):
    mapping = {
        "inform": "nod",
        "question": "tilt_head",
        "persuade": "point",
        "agree": "smile",
        "challenge": "frown",
        "deceive": "shrug"
    }
    return mapping.get(intent, "idle")

def infer_emotion(intent, confidence):
    if intent in ["challenge", "deceive"]:
        return "tense"
    if confidence > 0.9:
        return "assertive"
    return "neutral"

# Example:
# export_unity_timeline("arena_1713057720", "aurora")