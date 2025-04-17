import json
import time
from pathlib import Path

def replay_conversation(session_id, delay=0.5, show_confidence=True):
    log_path = Path(f"../../conversation/logs/{session_id}.traininglog")

    if not log_path.exists():
        print(f"[REPLAY] Log file not found for session: {session_id}")
        return

    print(f"\n[REPLAY START] Session: {session_id}")
    with open(log_path, 'r') as f:
        turns = f.readlines()

    for line in turns:
        turn = json.loads(line)
        speaker = turn.get("from_agent")
        msg = turn.get("message")
        intent = turn.get("intent", "inform")
        confidence = turn.get("confidence", 0.5)

        display = f"{speaker}: \"{msg}\"  ({intent}"
        if show_confidence:
            display += f", conf={confidence:.2f})"
        else:
            display += ")"

        print(display)
        time.sleep(delay)

    print("\n[REPLAY END]\n")

# Example usage:
# replay_conversation("arena_1713057720", delay=0.3)