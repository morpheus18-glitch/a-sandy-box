import json
from pathlib import Path
from datetime import datetime
from backend.agents.identity_synthesizer import synthesize_agent_identity

def create_agent_v2(template_path):
    with open(template_path, 'r') as f:
        data = json.load(f)

    agent_id = data["agent_id"]
    memory_path = Path(f"../../agents/memory/{agent_id}_memory.json")
    mcp_path = Path(f"../../protocols/mcp/{agent_id}.mcp")
    appearance_path = Path(f"../../agents/visuals/{agent_id}_appearance.json")

    # === Build Memory ===
    traits = data.get("core_traits", {
        "confidence": 0.5,
        "eloquence": 0.5,
        "empathy": 0.5,
        "strategic_thinking": 0.5,
        "leadership": 0.5
    })

    memory = {
        "agent_id": agent_id,
        "created_at": datetime.utcnow().isoformat(),
        "traits": traits,
        "memory_log": [],
        "milestones": ["Initialized via agent_creator_v2.py"],
        "lineage": {
            "parent": None,
            "descendants": []
        }
    }

    with open(memory_path, 'w') as f:
        json.dump(memory, f, indent=2)

    # === Build MCP ===
    mcp = {
        "agent_id": agent_id,
        "model_id": data.get("model_id", "local-stub"),
        "archetype": data.get("metadata", {}).get("archetype", "undefined"),
        "species": data.get("metadata", {}).get("species", "human"),
        "pronouns": data.get("metadata", {}).get("pronouns", ["they"]),
        "gesture_profile": data.get("behavior_sync", {}).get("gesture_profile", "neutral"),
        "default_intents": data.get("default_intents", ["inform"]),
        "voice_style": data.get("voice_style", "neutral"),
        "alignment": data.get("personality_kernel", {}).get("alignment", "neutral")
    }

    with open(mcp_path, 'w') as f:
        json.dump(mcp, f, indent=2)

    # === Save Appearance Payload ===
    visual_bundle = {
        "appearance": data.get("appearance", {}),
        "anatomy": data.get("anatomy", {}),
        "surface_features": data.get("surface_features", {}),
        "style_layering": data.get("style_layering", {}),
        "accessory_clusters": data.get("accessory_clusters", {}),
        "movement_tags": data.get("behavior_sync", {}),
    }

    with open(appearance_path, 'w') as f:
        json.dump(visual_bundle, f, indent=2)

    # === Identity Profile ===
    synthesize_agent_identity(agent_id)

    print(f"[AGENT_CREATOR_V2] Agent '{agent_id}' created successfully.")

# Example usage:
# create_agent_v2("../../agents/templates/agent_character.schema.v2.json")