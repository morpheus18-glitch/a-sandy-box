import json
import os
from pathlib import Path
from datetime import datetime

BASE = Path("../../agents")

def create_identity(agent_id):
    identity = {
        "agent_id": agent_id,
        "created_at": datetime.now().isoformat(),
        "name": agent_id.capitalize(),
        "role": "dialogue agent",
        "purpose": "engage in recursive reasoning",
        "version": "1.0",
        "traits": {
            "confidence": 0.5,
            "empathy": 0.5,
            "curiosity": 0.5,
            "leadership": 0.4
        },
        "keywords": [],
        "memory_enabled": True
    }
    path = BASE / "identity" / f"{agent_id}_identity.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    json.dump(identity, open(path, 'w'), indent=2)
    print(f"[+] Identity: {path}")

def create_visual(agent_id):
    from agent_visual_builder import build_agent_visual_config
    build_agent_visual_config(agent_id)

def create_abp(agent_id):
    abp = {
        "agent_id": agent_id,
        "version": "1.0",
        "pose_mapping": {
            "inform": "explain_pose",
            "challenge": "lean_forward",
            "agree": "open_chest_nod"
        },
        "gesture_mapping": {
            "neutral": "hand_rest",
            "emotional": "open_palm_reach"
        },
        "emotion_blend_profiles": {
            "confidence_high": {"stance": "upright", "face": "intense"},
            "empathy_high": {"gaze": "soft", "hands": "gentle"}
        },
        "feedback_loops": {
            "sync_loss": {
                "trigger": "contradiction_count > 3",
                "effect": "glitch_behavior",
                "suppress_behavior": True,
                "override_voice": "distorted"
            }
        },
        "training_mode": {
            "enabled": True,
            "reward_style": "stability",
            "evolution_trait": "expressiveness"
        }
    }
    path = Path("../../protocols/abp") / f"{agent_id}.abp"
    path.parent.mkdir(parents=True, exist_ok=True)
    json.dump(abp, open(path, 'w'), indent=2)
    print(f"[+] ABP: {path}")

def create_mcp(agent_id, model="gpt-4"):
    mcp = {
        "agent_id": agent_id,
        "model": model,
        "temperature": 0.75,
        "max_tokens": 2048,
        "system_prompt": f"You are {agent_id}, an adaptive reasoning agent in a simulated environment.",
        "allow_function_calls": True,
        "persona": "insightful, expressive, honest",
        "mode": "safe"
    }
    path = Path("../../protocols/mcp") / f"{agent_id}.mcp"
    path.parent.mkdir(parents=True, exist_ok=True)
    json.dump(mcp, open(path, 'w'), indent=2)
    print(f"[+] MCP: {path}")

def run_creator(agent_id):
    create_identity(agent_id)
    create_visual(agent_id)
    create_abp(agent_id)
    create_mcp(agent_id)
    print(f"[✓] Agent {agent_id} created successfully.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Create a full agent package")
    parser.add_argument("agent_id", type=str, help="Name of the agent to create")
    args = parser.parse_args()

    run_creator(args.agent_id)