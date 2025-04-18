import json
import zipfile
from pathlib import Path
import shutil

def resurrect_agent_from_archive(archive_path):
    """
    Extracts an export archive (.qpak.zip or .simstate.zip) and reinstates agent state files
    into the live project directories.
    
    Parameters:
      - archive_path: Path to the zip archive export.
      
    Expected Archive Structure:
      /<archive_folder>/
         session.arena
         session.traininglog
         session.analysis
         manifest.json
         /agents/
             <agent_id>_memory.json
             <agent_id>_identity.json
         ... (other optional files)
    """
    archive_file = Path(archive_path)
    if not archive_file.exists():
        raise FileNotFoundError(f"[RESURRECTION] Archive not found: {archive_path}")

    extract_dir = archive_file.with_suffix('')  # Remove .zip suffix for folder name
    if extract_dir.exists():
        shutil.rmtree(extract_dir)  # Clean existing folder if any
    extract_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(archive_file, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    print(f"[RESURRECTION] Extracted archive to: {extract_dir}")

    # Check for agent state directory in the archive.
    agents_dir = extract_dir / "agents"
    if not agents_dir.exists():
        raise FileNotFoundError(f"[RESURRECTION] Agent state directory missing in archive: {agents_dir}")

    # Define live destination directories.
    live_memory_dir = Path("../../agents/memory/")
    live_identity_dir = Path("../../agents/identity/")

    # Copy each agent's memory and identity file from the archive into the live folders.
    for file in agents_dir.glob("*_memory.json"):
        dest = live_memory_dir / file.name
        shutil.copy(file, dest)
        print(f"[RESURRECTION] Restored memory: {dest}")

    for file in agents_dir.glob("*_identity.json"):
        dest = live_identity_dir / file.name
        shutil.copy(file, dest)
        print(f"[RESURRECTION] Restored identity: {dest}")

    # Optionally, update MCP files if included in the archive (if not, they remain unchanged).
    mcp_archive_dir = extract_dir / "mcp"
    if mcp_archive_dir.exists():
        live_mcp_dir = Path("../../protocols/mcp/")
        for file in mcp_archive_dir.glob("*.mcp"):
            dest = live_mcp_dir / file.name
            shutil.copy(file, dest)
            print(f"[RESURRECTION] Restored MCP: {dest}")

    print("[RESURRECTION] Agent resurrection complete.")
    return True

# Example usage:
# resurrect_agent_from_archive("../../exports/arena_social_ethics_test_archive.zip")