import json
from pathlib import Path
from datetime import datetime
import random

def generate_agent_template():
    print("=== [AGENT DESIGNER V2] ===")
    agent_id = input("Agent ID: ").strip().lower()
    display_name = input("Display Name: ").strip()
    archetype = input("Archetype (e.g., diplomat, tactician, rogue AI): ").strip()
    species = input("Species (human, android, alien, hybrid): ").strip() or "human"
    gender = input("Gender Identity (male, female, fluid, constructed): ").strip() or "non-binary"
    model_id = input("Model ID (gpt-4o, claude-3-sonnet, local-stub): ").strip() or "local-stub"

    print("\n-- Physical Appearance --")
    height = int(input("Height (cm): ") or 180)
    build = input("Build (slim, athletic, bulky): ") or "athletic"
    skin_tone = input("Skin tone: ") or "medium"
    eye_color = input("Eye color: ") or "hazel"
    hair_style = input("Hair style (long, buzz, coils, cyber): ") or "buzz"
    hair_color = input("Hair color: ") or "black"

    print("\n-- Clothing & Accessories --")
    outfit = input("Preset outfit (field_rig, mystic_robe, urban): ") or "field_rig"
    accessories = input("Accessories (comma-separated): ") or "visor, pendant"
    accessories = [a.strip() for a in accessories.split(",")]

    print("\n-- Behavioral Core --")
    confidence = float(input("Confidence (0.0 - 1.0): ") or "0.6")
    empathy = float(input("Empathy (0.0 - 1.0): ") or "0.5")
    eloquence = float(input("Eloquence (0.0 - 1.0): ") or "0.7")
    strategy = float(input("Strategic Thinking (0.0 - 1.0): ") or "0.65")
    leadership = float(input("Leadership (0.0 - 1.0): ") or "0.55")

    gesture_style = input("Gesture Style (animated, subtle, serpentine): ") or "subtle"
    intent_bias = input("Dominant Intents (comma-separated): ") or "inform,agree"
    intent_bias = [i.strip() for i in intent_bias.split(",")]

    # Final structure
    template = {
        "agent_id": agent_id,
        "display_name": display_name,
        "metadata": {
            "archetype": archetype,
            "species": species,
            "gender_identity": gender,
            "pronouns": ["they"]
        },
        "model_id": model_id,
        "anatomy": {
            "height_cm": height,
            "build": build,
            "skeletal_proportions": {
                "torso_ratio": 0.5,
                "leg_ratio": 0.5,
                "arm_span_ratio": 1.0,
                "neck_length": 0.15,
                "head_proportion": 0.12
            }
        },
        "surface_features": {
            "skin": {
                "tone": skin_tone,
                "texture": "smooth"
            },
            "hair": {
                "style": hair_style,
                "color": hair_color
            },
            "eye": {
                "iris_color": eye_color,
                "shape": "round",
                "pupil_type": "round"
            }
        },
        "style_layering": {
            "full_outfits": [outfit]
        },
        "accessory_clusters": {
            "head": [a for a in accessories if a in ["visor", "crown"]],
            "neck": [a for a in accessories if a in ["pendant", "scarf"]],
            "hands": [a for a in accessories if a in ["rings", "gloves"]]
        },
        "behavior_sync": {
            "gesture_profile": gesture_style,
            "movement_rhythm": "smooth"
        },
        "core_traits": {
            "confidence": confidence,
            "empathy": empathy,
            "eloquence": eloquence,
            "strategic_thinking": strategy,
            "leadership": leadership
        },
        "default_intents": intent_bias
    }

    save_path = Path(f"../../agents/templates/{agent_id}.agent.json")
    with open(save_path, 'w') as f:
        json.dump(template, f, indent=2)

    print(f"\n[DESIGNER] Agent template saved to: {save_path}")
    return save_path

# Usage:
# Run this file to begin character creation
# Then use `agent_creator_v2.py` to instantiate the agent