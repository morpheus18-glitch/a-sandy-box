import os
import json
import shutil
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("../../")
ARCHIVE_DIR = BASE_DIR / "archives"
TARGETS = [
    "agents/identity",
    "agents/visuals",
    "agents/memory",
    "protocols/mcp",
    "protocols/abp",
    "conversation/logs",
    "unity_exports",
    "rdip",
    "training_logs"
]

def archive_session(session_id):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_path = ARCHIVE_DIR / f"{session_id}_{timestamp}"
    archive_path.mkdir(parents=True, exist_ok=True)

    for target in TARGETS:
        src = BASE_DIR / target
        dst = archive_path / target
        if src.exists():
            shutil.copytree(src, dst, dirs_exist_ok=True)
            print(f"[ARCHIVE] Copied: {target}")

    print(f"[✓] Session '{session_id}' archived to {archive_path}")

def restore_session(archive_name):
    archive_path = ARCHIVE_DIR / archive_name
    if not archive_path.exists():
        raise FileNotFoundError(f"Archive '{archive_name}' not found.")

    for target in TARGETS:
        src = archive_path / target
        dst = BASE_DIR / target
        if src.exists():
            shutil.copytree(src, dst, dirs_exist_ok=True)
            print(f"[RESTORE] Restored: {target}")

    print(f"[✓] Archive '{archive_name}' restored into active session directories.")