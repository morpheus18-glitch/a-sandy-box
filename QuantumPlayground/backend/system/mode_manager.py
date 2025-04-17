import json
from pathlib import Path

AGENT_MODE_PATH = "../../settings/agent_mode_config.json"
LEVELS = ["none", "minor", "moderate", "allow_any"]

def load_agent_mode_config():
    with open(AGENT_MODE_PATH, 'r') as f:
        return json.load(f)

def is_allowed(agent_id, category, level_required):
    config = load_agent_mode_config()
    agent_rules = config.get("agents", {}).get(agent_id, {})
    default_rules = config.get("default", {})

    agent_setting = agent_rules.get(category, default_rules.get(category, "none"))

    try:
        return LEVELS.index(agent_setting) >= LEVELS.index(level_required)
    except ValueError:
        return False

def detect_conflicting_restrictions():
    config = load_agent_mode_config()
    strict_flags = {}

    for agent_id, rules in config.get("agents", {}).items():
        for category, level in rules.items():
            if level == "none":
                strict_flags.setdefault(category, []).append(agent_id)

    return strict_flags