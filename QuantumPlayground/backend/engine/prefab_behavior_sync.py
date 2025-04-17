import json
from pathlib import Path

def sync_behavior_from_prefab(agent_id):
    prefab_path = Path(f"../../unity_exports/{agent_id}_prefab.json")
    if not prefab_path.exists():
        print(f"[SYNC] Missing prefab for: {agent_id}")
        return {}

    with open(prefab_path, 'r') as f:
        prefab = json.load(f)

    anim_tags = prefab.get("animation_tags", [])
    gesture = prefab.get("gesture_profile", "neutral")
    movement = prefab.get("movement_rhythm", "smooth")
    voice = prefab.get("voice_style", "neutral")

    return {
        "animation_tags": anim_tags,
        "gesture_profile": gesture,
        "movement_style": movement,
        "voice_profile": voice
    }

# Example usage in conversation loop:
# visuals = sync_behavior_from_prefab("zenith")
# apply_anim_states(agent_id, visuals["animation_tags"])