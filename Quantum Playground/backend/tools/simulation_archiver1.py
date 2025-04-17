import json
import os
import shutil
from pathlib import Path
from datetime import datetime

def archive_simulation(session_id):
    """
    Bundles all logs, analysis, arena metadata, agent snapshots, and traits into a single export folder.
    """
    base_path = Path("../../conversation/")
    export_root = Path("../../exports/") / f"{session_id}_archive"
    export_root.mkdir(parents=True, exist_ok=True)

    # Copy arena metadata
    copy_if_exists(base_path / "sessions" / f"{session_id}.arena", export_root / "session.arena")
    copy_if_exists(base_path / "logs" / f"{session_id}.traininglog", export_root / "session.traininglog")
    copy_if_exists(base_path / "logs" / f"{session_id}.analysis", export_root / "session.analysis")

    # Parse arena to locate agents
    arena_path = base_path / "sessions" / f"{session_id}.arena"
    if not arena_path.exists():
        print(f"[ARCHIVE] Arena metadata missing.")
        return

    with open(arena_path, 'r') as f:
        arena = json.load(f)

    agents = arena.get("agents", [])
    export_agent_states(agents, export_root / "agents")

    # Optional: add timestamp & manifest
    meta = {
        "session_id": session_id,
        "timestamp": datetime.utcnow().isoformat(),
        "agents": agents,
        "prompt_id": arena.get("prompt_id"),
        "rounds": arena.get("rounds"),
        "export_version": "1.0"
    }

    with open(export_root / "manifest.json", 'w') as f:
        json.dump(meta, f, indent=2)

    print(f"[ARCHIVE] Simulation exported to: {export_root}")

def copy_if_exists(src, dst):
    if src.exists():
        shutil.copyfile(src, dst)
    else:
        print(f"[ARCHIVE] Missing file: {src.name}")

def export_agent_states(agent_ids, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    for agent_id in agent_ids:
        trait_path = Path(f"../../agents/memory/{agent_id}_memory.json")
        identity_path = Path(f"../../agents/identity/{agent_id}.identity.json")

        if trait_path.exists():
            shutil.copyfile(trait_path, output_dir / f"{agent_id}_memory.json")
        if identity_path.exists():
            shutil.copyfile(identity_path, output_dir / f"{agent_id}_identity.json")

# Example:
# archive_simulation("arena_1713057720")