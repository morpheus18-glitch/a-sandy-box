import json
import zipfile
from pathlib import Path

def bundle_prefab_assets(agent_id):
    paths = {
        "prefab": Path(f"../../unity_exports/{agent_id}_prefab.json"),
        "appearance": Path(f"../../agents/visuals/{agent_id}_appearance.json"),
        "identity": Path(f"../../agents/identity/{agent_id}.identity.json"),
        "mcp": Path(f"../../protocols/mcp/{agent_id}.mcp")
    }

    for label, path in paths.items():
        if not path.exists():
            raise FileNotFoundError(f"[BUNDLER] Missing {label} file: {path}")

    out_path = Path(f"../../unity_exports/{agent_id}.qpak.zip")
    with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as bundle:
        for label, path in paths.items():
            bundle.write(path, arcname=path.name)

    print(f"[BUNDLER] Prefab asset kit saved: {out_path}")
    return out_path

# Example:
# bundle_prefab_assets("zenith")