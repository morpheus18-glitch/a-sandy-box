import json
from pathlib import Path
from datetime import datetime

def export_unreal_asset(agent_template_path):
    with open(agent_template_path, 'r') as f:
        agent = json.load(f)

    agent_id = agent["agent_id"]
    anatomy = agent.get("anatomy", {})
    surface = agent.get("surface_features", {})
    outfit = agent.get("style_layering", {}).get("full_outfits", [])
    accessories = agent.get("accessory_clusters", {})

    asset = {
        "UnrealAsset": {
            "AssetName": agent_id,
            "SkeletonRig": select_rig(anatomy),
            "MeshData": {
                "BaseSkin": surface.get("skin", {}).get("texture", "default"),
                "HairStyle": surface.get("hair", {}).get("style", "none"),
                "HairColor": surface.get("hair", {}).get("color", "black"),
                "EyeShape": surface.get("eye", {}).get("shape", "round"),
                "EyeColor": surface.get("eye", {}).get("iris_color", "gray")
            },
            "ClothingLayers": outfit,
            "AccessoryMap": accessories,
            "TraitDrivenAnim": {
                "Confidence": agent["core_traits"]["confidence"],
                "Leadership": agent["core_traits"]["leadership"],
                "Eloquence": agent["core_traits"]["eloquence"]
            },
            "Metadata": {
                "Created": datetime.utcnow().isoformat(),
                "Author": "QuantumPlayground Exporter v1"
            }
        }
    }

    out_path = Path(f"../../unity_exports/{agent_id}.ueasset.json")
    with open(out_path, 'w') as f:
        json.dump(asset, f, indent=2)

    print(f"[UEASSET EXPORTER] Exported: {out_path}")
    return out_path

def select_rig(anatomy):
    if anatomy.get("appendages", {}).get("wing_type") != "none":
        return "HumanoidWinged"
    if anatomy.get("appendages", {}).get("tail_type") != "none":
        return "HumanoidWithTail"
    return "StandardHumanoid"

# Example:
# export_unreal_asset("../../agents/templates/zenith.agent.json")