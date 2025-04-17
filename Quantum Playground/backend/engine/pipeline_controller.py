from backend.engine.orchestration_engine import prepare_simulation, post_simulation_pipeline
from backend.simulation.forked_arena_generator import fork_arena
from backend.simulation.recursive_arena_trainer import train_from_forked_arenas
import time

def run_pipeline(base_session_id, agent_ids, prompt_file, forks=3, rounds=10):
    """
    Runs a base simulation, forks multiple variants, runs all, and processes training feedback.
    """
    print(f"\n=== [PIPELINE START] ===")
    print(f"Running base session: {base_session_id}")

    # Run base
    controller = prepare_simulation(base_session_id, agent_ids, prompt_file, rounds)
    # controller.start_conversation()  # Paused until all systems confirmed
    post_simulation_pipeline(base_session_id, agent_ids)

    fork_ids = []
    for i in range(forks):
        vid = f"v{i+1}"
        forked_session = fork_arena(base_session_id, variation_id=vid, clone_agents=True)
        fork_ids.append(vid)
        fork_agents = get_agents_from_arena(forked_session)

        controller = prepare_simulation(forked_session, fork_agents, prompt_file, rounds)
        # controller.start_conversation()  # Paused
        post_simulation_pipeline(forked_session, fork_agents)

        time.sleep(0.5)

    print(f"\n[PIPELINE] All forks complete. Beginning recursive training...")
    train_from_forked_arenas(base_session_id, fork_ids)

    print(f"\n=== [PIPELINE END] ===")

def get_agents_from_arena(session_id):
    from pathlib import Path
    import json
    arena_path = Path(f"../../conversation/sessions/{session_id}.arena")
    if not arena_path.exists():
        return []
    with open(arena_path, 'r') as f:
        return json.load(f).get("agents", [])

# Example:
# run_pipeline("arena_ethics_test", ["zenith", "aurora"], "../../conversation/prompts/dlg_social_ethics_001.dlg", forks=2)