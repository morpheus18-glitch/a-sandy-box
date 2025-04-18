import json
from pathlib import Path

def analyze_pose_deltas(session_id, agent_id):
    path = Path(f"../../conversation/logs/{session_id}_{agent_id}.timeline")
    if not path.exists():
        raise FileNotFoundError(f"[DELTA ANALYZER] Timeline not found: {path}")

    with open(path, 'r') as f:
        entries = json.load(f)

    pose_changes = []
    prev_pose = None
    for entry in entries:
        pose = entry["animation_state"].get("pose")
        if prev_pose and pose != prev_pose:
            pose_changes.append({
                "from": prev_pose,
                "to": pose,
                "at": entry["timestamp"]
            })
        prev_pose = pose

    print(f"[DELTA] {agent_id} pose changes:")
    for change in pose_changes:
        print(f" - {change['from']} → {change['to']} at {change['at']}")
    return pose_changes