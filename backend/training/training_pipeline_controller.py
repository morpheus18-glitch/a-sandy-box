import json
from pathlib import Path
from datetime import datetime

IDENTITY_DIR = Path("../../agents/identity/")
MEMORY_DIR = Path("../../agents/memory/")
RDiP_DIR = Path("../../rdip/")
LOG_DIR = Path("../../conversation/logs/")
TRAINING_LOG = Path("../../training_logs/")
TRAINING_LOG.mkdir(parents=True, exist_ok=True)

def run_all_pipelines(session_id, agent_ids):
    for agent_id in agent_ids:
        print(f"[TRAINING] Running pipeline for: {agent_id}")
        update_traits_from_rdip(agent_id, session_id)

def update_traits_from_rdip(agent_id, session_id):
    rdip_path = RDiP_DIR / f"{session_id}_{agent_id}_rdip.json"
    identity_path = IDENTITY_DIR / f"{agent_id}_identity.json"

    if not rdip_path.exists() or not identity_path.exists():
        print(f"[WARN] Missing files for {agent_id}, skipping.")
        return

    with open(rdip_path, 'r') as f:
        rdip = json.load(f)

    with open(identity_path, 'r') as f:
        identity = json.load(f)

    traits = identity.get("traits", {})

    # Adapt trait logic
    traits["confidence"] = adjust(traits.get("confidence", 0.5), rdip["self_reference"], 0.02)
    traits["curiosity"] = adjust(traits.get("curiosity", 0.5), rdip["recursive_mentions"], 0.015)
    traits["empathy"] = adjust(traits.get("empathy", 0.5), rdip["avg_sentiment"], 0.01)
    traits["leadership"] = adjust(traits.get("leadership", 0.5), rdip["leadership_signals"], 0.025)

    identity["traits"] = traits

    with open(identity_path, 'w') as f:
        json.dump(identity, f, indent=2)

    log_training(agent_id, session_id, traits)

def adjust(current, signal, factor):
    delta = signal * factor
    updated = round(max(0.0, min(1.0, current + delta)), 3)
    return updated

def log_training(agent_id, session_id, traits):
    path = TRAINING_LOG / f"{agent_id}_{session_id}_training.json"
    log = {
        "agent_id": agent_id,
        "session_id": session_id,
        "timestamp": datetime.now().isoformat(),
        "updated_traits": traits
    }
    with open(path, 'w') as f:
        json.dump(log, f, indent=2)
    print(f"[✓] Traits updated for {agent_id}")