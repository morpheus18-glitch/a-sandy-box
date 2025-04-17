from backend.ml.trait_reinforcement_trainer import run_trait_reinforcement
from backend.ml.intent_sequence_learner import run_intent_sequence_learning
from backend.ml.memory_embedding_engine import run_memory_embedding
from backend.ml.nesi_engine import run_nesi_swarm
from backend.analysis.rdip_tracker import track_rdip
from backend.analysis.rdip_evolution_handler import evolve_agent_by_rdip
from backend.protocols.abp_evolution_engine import evolve_abp

def run_all_pipelines(session_id, agent_ids):
    print(f"\n[ML_PIPELINE] Running full simulation ML pipeline: {session_id}")

    for agent_id in agent_ids:
        print(f"\n--- AGENT: {agent_id.upper()} ---")

        # Trait training
        run_trait_reinforcement(session_id, agent_id)

        # Intent learning
        run_intent_sequence_learning(session_id, agent_id)

        # Memory vector embedding
        run_memory_embedding(session_id, agent_id)

        # RDiP tracking & evolution
        track_rdip(session_id, agent_id)
        evolve_agent_by_rdip(agent_id)

        # ABP evolution (adaptive physical behavior)
        evolve_abp(agent_id, session_id)

    # Run NESI last—requires full population embedding
    run_nesi_swarm(agent_ids, session_id)

    print(f"\n[ML_PIPELINE] All pipelines complete.")