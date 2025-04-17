import json
from pathlib import Path
from datetime import datetime

from backend.protocols.abp_controller import resolve_abp_response
from backend.protocols.cnip_processor import process_crowd_input
from backend.protocols.ietsc_classifier import classify_ietsc
from backend.inference.model_router import route_model_query

LOG_PATH = Path("../../conversation/logs/")
TRACK_PATH = Path("../../unity_exports/")
MEMORY_PATH = Path("../../agents/memory/")

def run_simulation_round(session_id, agents, turn, prompt):
    for i, agent in enumerate(agents):
        agent_id = agent["id"]
        abp = agent["abp"]
        memory = load_memory(agent_id)

        # CNIP resolves crowd signal
        incoming = build_crowd_messages(agents, agent_id)
        cnip = process_crowd_input(agent_id, incoming)
        primary = cnip.get("primary")
        acknowledges = cnip.get("acknowledge")

        # Build contextualized prompt
        full_prompt = build_prompt(agent_id, prompt, turn, primary, acknowledges)
        response = route_model_query(agent_id, full_prompt, memory)

        # Classify using IETSC
        ai_state = classify_ietsc(agent_id, response)

        # ABP Resolution
        pose = resolve_abp_response(abp, ai_state)

        # Log outputs
        log_timeline(session_id, agent_id, turn, response, ai_state, pose)
        log_animtrack(session_id, agent_id, turn, response, ai_state, pose)

        print(f"[{agent_id}] ({ai_state['intent']} / {ai_state['emotion']}): {response[:70]}...")

def load_memory(agent_id):
    path = MEMORY_PATH / f"{agent_id}_memory.json"
    if not path.exists(): return []
    return json.load(open(path, 'r'))

def build_crowd_messages(agents, current_id):
    return [
        {
            "from": a["id"],
            "message": f"{a['id']} spoke previously.",
            "tone": "neutral",
            "intent": "inform",
            "priority": 0.5
        }
        for a in agents if a["id"] != current_id
    ]

def build_prompt(agent_id, prompt, turn, primary, acknowledges):
    base = f"You are Agent '{agent_id}'. Turn {turn}. "
    if primary:
        base += f"Primary speaker last turn: {primary}. "
    if acknowledges:
        base += f"Acknowledged: {', '.join(acknowledges)}. "

    base += f"\nPrompt: {prompt}\nRespond in character."
    return base

def log_timeline(session_id, agent_id, turn, message, ai_state, pose):
    timeline_file = LOG_PATH / f"{session_id}_{agent_id}.timeline"
    LOG_PATH.mkdir(parents=True, exist_ok=True)

    entry = {
        "turn": turn,
        "timestamp": datetime.now().isoformat(),
        "message": message,
        "intent": ai_state["intent"],
        "emotion": ai_state["emotion"],
        "tone": ai_state["tone"],
        "sentiment": ai_state["sentiment"],
        "contradictions": ai_state["contradictions"],
        "animation_state": {
            "pose": pose.get("pose", "idle"),
            "gesture": pose.get("gesture", "hand_rest")
        },
        "expression_state": {
            "expression": pose.get("face", "neutral"),
            "blendshapes": pose.get("blendshapes", {})
        }
    }

    data = []
    if timeline_file.exists():
        data = json.load(open(timeline_file))
    data.append(entry)

    json.dump(data, open(timeline_file, 'w'), indent=2)

def log_animtrack(session_id, agent_id, turn, message, ai_state, pose):
    track_file = TRACK_PATH / f"{agent_id}_{session_id}_animtrack.json"
    TRACK_PATH.mkdir(parents=True, exist_ok=True)

    frame = {
        "frame": turn,
        "pose": pose.get("pose", "idle"),
        "gesture": pose.get("gesture", "hand_rest"),
        "expression": pose.get("face", "neutral"),
        "blendshapes": pose.get("blendshapes", {}),
        "line": message,
        "tone": ai_state["tone"],
        "intent": ai_state["intent"],
        "sentiment": ai_state["sentiment"]
    }

    data = []
    if track_file.exists():
        data = json.load(open(track_file))
    data.append(frame)

    json.dump(data, open(track_file, 'w'), indent=2)