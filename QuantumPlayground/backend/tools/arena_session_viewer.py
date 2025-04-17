import json
from pathlib import Path

def view_arena_session(session_id):
    arena_path = Path(f"../../conversation/sessions/{session_id}.arena")
    log_path = Path(f"../../conversation/logs/{session_id}.traininglog")
    analysis_path = Path(f"../../conversation/logs/{session_id}.analysis")

    if not arena_path.exists():
        print(f"[VIEWER] Arena file not found for session: {session_id}")
        return

    with open(arena_path, 'r') as f:
        arena = json.load(f)

    print("\n===== ARENA SESSION OVERVIEW =====")
    print(f"Session ID   : {arena['session_id']}")
    print(f"Agents       : {arena['agents']}")
    print(f"Prompt       : {arena['prompt_id']}")
    print(f"Rounds       : {arena['rounds']}")
    print("----------------------------------")

    if analysis_path.exists():
        with open(analysis_path, 'r') as f:
            analysis = json.load(f)

        print("\n===== BEHAVIORAL ANALYSIS =====")
        print(f"Emergent Leader : {analysis.get('emergent_leader')}")
        print(f"Dominant Intents: {json.dumps(analysis.get('dominant_intents', {}), indent=2)}")
        print(f"RDiP Flags      : {json.dumps(analysis.get('rdip_flags', {}), indent=2)}")
    else:
        print("\n[INFO] No analysis file found.")

    if log_path.exists():
        with open(log_path, 'r') as f:
            turns = f.readlines()
        print(f"\n===== LOG SUMMARY =====")
        print(f"Total Turns: {len(turns)}")
        print("Last 3 Turns:")
        for line in turns[-3:]:
            turn = json.loads(line)
            print(f" - [{turn['from_agent']}] {turn['message']} ({turn['intent']})")

    print("\nExport complete.\n")

# Example call:
# view_arena_session("arena_1713057720")