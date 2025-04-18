import json
from pathlib import Path

def generate_agent_timeline(agent_id):
    memory_path = Path(f"../../agents/memory/{agent_id}_memory.json")
    session_dir = Path("../../conversation/sessions/")
    analysis_dir = Path("../../conversation/logs/")

    if not memory_path.exists():
        print(f"[TIMELINE] Memory not found.")
        return

    with open(memory_path, 'r') as f:
        memory = json.load(f)

    print(f"\n===== AGENT TIMELINE: {agent_id.upper()} =====")
    print(f"Created at: {memory['created_at']}")
    print(f"Total Events: {len(memory['memory_log'])}")

    sessions = []
    for f in session_dir.glob("*.arena"):
        with open(f, 'r') as s:
            data = json.load(s)
            if agent_id in data.get("agents", []):
                sessions.append(data["session_id"])

    print(f"\nSessions Participated In:")
    for s in sessions:
        print(f" - {s}")

    print(f"\nLinked Analysis Files:")
    for s in sessions:
        analysis_path = analysis_dir / f"{s}.analysis"
        if analysis_path.exists():
            print(f" * {s}.analysis")

# Example:
# generate_agent_timeline("zenith")