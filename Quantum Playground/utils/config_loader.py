import yaml
from pathlib import Path

def load_config(path="../../config/simulation_config.yaml"):
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"[CONFIG] Missing config file: {path}")

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config