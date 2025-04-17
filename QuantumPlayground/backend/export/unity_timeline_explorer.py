import json
from pathlib import Path

def export_to_unity_timeline(session_id, agent_id):
    input_path = Path(f"../../conversation/logs/{session_id}_{agent_id}.timeline")
    output_path = Path(f"../../unity_exports/{agent_id}_{session_id}.unitytimeline")

    if not input_path.exists():
        raise FileNotFoundError(f"[EXPORTER] Timeline missing: {input_path}")

    with open(input_path, 'r') as f:
        timeline = json.load(f)

    unity_events = []
    for entry in timeline:
        event = {
            "time": entry["timestamp"],
            "pose": entry["animation_state"].get("pose"),
            "gesture": entry["animation_state"].get("gesture"),
            "expression": entry["expression_state"].get("expression"),
            "blendshapes": entry["expression_state"].get("blendshapes", {}),
            "line": entry["message"]
        }
        unity_events.append(event)

    with open(output_path, 'w') as f:
        json.dump(unity_events, f, indent=2)

    print(f"[UNITY EXPORT] Saved timeline: {output_path}")