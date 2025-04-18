import json
import time
from pathlib import Path
from backend.export.live_stream_sim_output import stream_animation_output

def replay_timeline(session_id, agent_id, playback_speed=1.0):
    """
    Replays a recorded timeline file to stream animation and expression back to prefab engines.
    """
    timeline_path = Path(f"../../conversation/logs/{session_id}_{agent_id}.timeline")
    if not timeline_path.exists():
        raise FileNotFoundError(f"[REPLAY] Timeline not found: {timeline_path}")

    with open(timeline_path, 'r') as f:
        timeline = json.load(f)

    print(f"[REPLAY] Starting replay for {agent_id} — {len(timeline)} frames")

    for entry in timeline:
        # Simulated playback delay
        time.sleep(0.5 / playback_speed)

        enriched_msg = {
            "message": entry["message"],
            "intent": entry["intent"],
            "tone": entry["tone"],
            "animation_state": entry["animation_state"],
            "expression_state": entry["expression_state"]
        }

        stream_animation_output(agent_id, enriched_msg)

    print(f"[REPLAY] Finished replay for {agent_id}.")

# Example usage:
# replay_timeline("arena_social_ethics_test", "zenith", playback_speed=1.5)