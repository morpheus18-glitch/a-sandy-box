import json
import os
from pathlib import Path
from datetime import datetime
from simulation_core import run_simulation_round
from ml_pipeline_controller import run_all_pipelines

CONFIG_PATH = Path("../../arena_configs/")

def load_config(file):
    with open(CONFIG_PATH / file, 'r') as f:
        return json.load(f)

def load_agent_data(agent_id):
    identity = json.load(open(Path(f"../../agents/identity/{agent_id}_identity.json")))
    abp = json.load(open(Path(f"../../protocols/abp/{agent_id}.abp")))
    mcp = json.load(open(Path(f"../../protocols/mcp/{agent_id}.mcp")))
    return {"id": agent_id, "identity": identity, "abp": abp, "mcp": mcp}

def run_arena(config_file):
    config = load_config(config_file)
    agents = [load_agent_data(agent_id) for agent_id in config["agents"]]
    prompt = config["prompt"]
    session_id = f"{config['session_name']}_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    print(f"\n[ARENA] Starting simulation: {session_id}")
    print(f"[ARENA] Prompt: {prompt}")
    print(f"[ARENA] Agents: {[a['id'] for a in agents]}")

    for turn in range(config["rounds"]):
        print(f"\n--- Turn {turn+1} ---")
        run_simulation_round(session_id, agents, turn, prompt)

    print(f"\n[ARENA] Simulation complete. Running ML pipeline...")
    run_all_pipelines(session_id, [a["id"] for a in agents])
    print(f"[✓] Arena session '{session_id}' exported successfully.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run a multi-agent simulation arena.")
    parser.add_argument("config", type=str, help="Arena config JSON filename")
    args = parser.parse_args()

    run_arena(args.config)