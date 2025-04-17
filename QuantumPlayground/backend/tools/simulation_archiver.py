import json
import os
import shutil
import zipfile
from pathlib import Path
from datetime import datetime
from backend.agents.identity_synthesizer import synthesize_agent_identity

def archive_simulation(session_id):
    """
    Bundles logs, analysis, arena, prompt, traits, and identity into a zipped export archive.
    """
    base_path = Path("../../conversation/")
    export_root = Path("../../exports/") / f"{session_id}_archive"
    export_root.mkdir(parents=True, exist_ok=True)

    # Copy session files
    copy_if_exists(base_path / "sessions" / f"{session_id}.arena", export_root / "session.arena")
    copy_if_exists(base_path / "logs" / f"{session_id}.traininglog", export_root / "session.traininglog")
    copy_if_exists(base_path / "logs" / f"{session_id}.analysis", export_root / "session.analysis")

    # Arena metadata
    arena_path = base_path / "sessions" / f"{session_id}.arena"
    if not arena_path.exists():
        print(f"[ARCHIVE] Arena metadata missing.")
        return

    with open(arena_path, 'r') as f:
        arena = json.load(f)

    agents = arena.get("agents", [])
    prompt_id = arena.get("prompt_id", "unknown")
    prompt_path = Path(f"../../conversation/prompts/{prompt_id}.dlg")
    if prompt_path.exists():
        shutil.copyfile(prompt_path, export_root / "session_prompt.dlg")

    # Export agent state
    export_agent_states(agents, export_root / "agents")

    # Write manifest
    meta = {
        "session_id": session_id,
        "timestamp": datetime.utcnow().isoformat(),
        "agents": agents,
        "prompt_id": prompt_id,
        "rounds": arena.get("rounds"),
        "export_version": "2.0"
    }

    with open(export_root / "manifest.json", 'w') as f:
        json.dump(meta, f, indent=2)

    # Create ZIP
    zip_path = Path("../../exports") / f"{session_id}_archive.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(export_root):
            for file in files:
                full_path = Path(root) / file
                arcname = full_path.relative_to(export_root.parent)
                zipf.write(full_path, arcname)

    print(f"[ARCHIVE] Export complete. Folder: {export_root.name}, Zip: {zip_path.name}")

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

        # Generate identity if missing
        if not identity_path.exists():
            identity = synthesize_agent_identity(agent_id)
            if identity:
                with open(identity_path, 'w') as f:
                    json.dump(identity, f, indent=2)

        if identity_path.exists():
            shutil.copyfile(identity_path, output_dir / f"{agent_id}_identity.json")