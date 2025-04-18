from backend.engine.pipeline_controller import run_pipeline
from backend.utils.config_loader import load_config
from pathlib import Path

def launch_simulation():
    config = load_config()

    base_session_id = config["session_id"]
    agents = config["agents"]
    prompt_file = config["prompt_file"]
    forks = config.get("forks", 1)
    rounds = config.get("rounds", 10)

    print(f"\n[BOOT] Loading config for session: {base_session_id}")
    print(f"[CONFIG] Agents: {agents} | Rounds: {rounds} | Forks: {forks}")

    run_pipeline(
        base_session_id=base_session_id,
        agent_ids=agents,
        prompt_file=prompt_file,
        forks=forks,
        rounds=rounds
    )

if __name__ == "__main__":
    launch_simulation()