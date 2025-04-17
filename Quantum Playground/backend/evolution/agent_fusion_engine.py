import json
import random
from pathlib import Path
from datetime import datetime

AGENT_DIR = Path("../../agents/")
FUSION_LOG = Path("../../fusion_logs/")
FUSION_LOG.mkdir(parents=True, exist_ok=True)

def fuse_agents(agent_a_id, agent_b_id, fused_id=None):
    fused_id = fused_id or f"{agent_a_id}_{agent_b_id}_fused_{datetime.now().strftime('%H%M%S')}"

    identity_a = load_json(AGENT_DIR / "identity" / f"{agent_a_id}_identity.json")
    identity_b = load_json(AGENT_DIR / "identity" / f"{agent_b_id}_identity.json")

    visual_a = load_json(AGENT_DIR / "visuals" / f"{agent_a_id}_visual.json")
    visual_b = load_json(AGENT_DIR / "visuals" / f"{agent_b_id}_visual.json")

    memory_a = load_json(AGENT_DIR / "memory" / f"{agent_a_id}_memory.json")
    memory_b = load_json(AGENT_DIR / "memory" / f"{agent_b_id}_memory.json")

    fused_identity = merge_identity(identity_a, identity_b, fused_id)
    fused_visual = merge_visual(visual_a, visual_b)
    fused_memory = memory_a + memory_b

    save_json(fused_identity, AGENT_DIR / "identity" / f"{fused_id}_identity.json")
    save_json(fused_visual, AGENT_DIR / "visuals" / f"{fused_id}_visual.json")
    save_json(fused_memory, AGENT_DIR / "memory" / f"{fused_id}_memory.json")

    log_fusion_event(agent_a_id, agent_b_id, fused_id)

    return fused_id

def merge_identity(a, b, fused_id):
    return {
        "agent_id": fused_id,
        "name": f"{a['name'][:3]}-{b['name'][-3:]}",
        "created_at": datetime.now().isoformat(),
        "role": "hybrid agent",
        "purpose": f"{a['purpose']} + {b['purpose']}",
        "traits": average_traits(a.get("traits", {}), b.get("traits", {})),
        "memory_enabled": True,
        "version": "fusion_1.0"
    }

def average_traits(t1, t2):
    keys = set(t1.keys()).union(t2.keys())
    return {k: round((t1.get(k, 0.5) + t2.get(k, 0.5)) / 2, 2) for k in keys}

def merge_visual(v1, v2):
    return {
        "species": random.choice([v1["species"], v2["species"]]),
        "bodyType": random.choice([v1["bodyType"], v2["bodyType"]]),
        "heightClass": random.choice([v1["heightClass"], v2["heightClass"]]),
        "skinTone": random.choice([v1["skinTone"], v2["skinTone"]]),
        "hairStyle": random.choice([v1["hairStyle"], v2["hairStyle"]]),
        "eyeColor": random.choice([v1["eyeColor"], v2["eyeColor"]]),
        "outfit": random.choice([v1["outfit"], v2["outfit"]]),
        "accessories": random.choice([v1["accessories"], v2["accessories"]]),
        "traits": {
            "nonHumanLimbs": v1["traits"]["nonHumanLimbs"] or v2["traits"]["nonHumanLimbs"],
            "extendedTorso": v1["traits"]["extendedTorso"] or v2["traits"]["extendedTorso"],
            "hasTail": v1["traits"]["hasTail"] or v2["traits"]["hasTail"],
            "voiceModPreset": random.choice([v1["traits"]["voiceModPreset"], v2["traits"]["voiceModPreset"]])
        }
    }

def log_fusion_event(a, b, fused_id):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "parent_a": a,
        "parent_b": b,
        "fused_id": fused_id
    }
    path = FUSION_LOG / f"{fused_id}_fusion.json"
    json.dump(entry, open(path, 'w'), indent=2)
    print(f"[FUSION] Created new agent: {fused_id}")

def load_json(path):
    return json.load(open(path, 'r'))

def save_json(data, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)