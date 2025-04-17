import json
from pathlib import Path
from datetime import datetime

def export_prefab(agent_template_path):
    with open(agent_template_path, 'r') as f:
        agent = json.load(f)

    agent_id = agent["agent_id"]
    appearance = agent.get("appearance", {})
    anatomy = agent.get("anatomy", {})
    surface = agent.get("surface_features", {})
    behavior = agent.get("behavior_sync", {})
    accessories = agent.get("accessory_clusters", {})
    outfit = agent.get("style_layering", {}).get("full_outfits", ["basic"])

    prefab = {
        "prefab_id": f"{agent_id}_prefab",
        "engine_target": "Unity | Unreal",
        "skeleton_rig": choose_skeleton(anatomy),
        "body_structure": anatomy,
        "skin": surface.get("skin", {}),
        "hair": surface.get("hair", {}),
        "eyes": surface.get("eye", {}),
        "gesture_profile": behavior.get("gesture_profile", "neutral"),
        "movement_rhythm": behavior.get("movement_rhythm", "smooth"),
        "dominant_pose_style": behavior.get("pose_dominance", "open"),
        "outfit_layers": outfit,
        "accessory_slots": accessories,
        "animation_tags": behavior.get("animation_tags", ["idle"]),
        "voice_style": agent.get("voice_style", "neutral"),
        "trait_sync": {
            "confidence": agent["core_traits"]["confidence"],
            "eloquence": agent["core_traits"]["eloquence"],
            "leadership": agent["core_traits"]["leadership"]
        },
        "metadata": {
            "source_agent": agent_id,
            "generated_at": datetime.utcnow().isoformat()
        }
    }

    out_path = Path(f"../../unity_exports/{agent_id}_prefab.json")
    with open(out_path, 'w') as f:
        json.dump(prefab, f, indent=2)

    print(f"[PREFAB EXPORTER] Exported prefab to: {out_path}")
    return out_path

def choose_skeleton(anatomy):
    limbs = anatomy.get("limb_traits", {}).get("alternate_limb_count", 0)
    wings = anatomy.get("appendages", {}).get("wing_type", "none")
    tail = anatomy.get("appendages", {}).get("tail_type", "none")

    if limbs > 2:
        return "multi_limb_rig"
    if wings != "none":
        return "winged_biped"
    if tail != "none":
        return "tailed_standard"
    return "standard_biped"

# Example:
# export_prefab("../../agents/templates/zenith.agent.json")