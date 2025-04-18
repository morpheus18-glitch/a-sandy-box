import json
from pathlib import Path
from backend.conversation.conversation_controller import ConversationArena
from backend.agents.behavior_weighting_engine import compute_behavior_weights
from backend.memory.memory_injection_engine import inject_agent_context
from backend.conversation.training_logger import TrainingLogger
from backend.agents.reward_scoring_engine import score_agent_performance
from backend.agents.trait_mutation_engine import mutate_agent_traits
from backend.agents.agent_promotion_engine import promote_agent_if_eligible
from backend.agents.behavior_summarizer import summarize_behavior_from_log
from backend.agents.identity_synthesizer import synthesize_agent_identity
from backend.memory.memory_threading_engine import build_memory_thread

def prepare_simulation(session_id, agents, prompt_path, rounds=10):
    print(f"\n[ORCHESTRATION] Initializing simulation: {session_id}")
    prompt = load_prompt(prompt_path)
    controller = ConversationArena(agent_ids=agents, prompt_file=prompt_path)
    controller.session_id = session_id
    controller.max_rounds = rounds
    controller.logger = TrainingLogger(session_id=session_id)

    print("[ORCHESTRATION] Injecting agent context & behavior profiles...")
    for aid in agents:
        context = inject_agent_context(aid)
        weights = compute_behavior_weights(aid)
        print(f" - {aid} context aligned: {context['meta_alignment']}")
        print(f" - {aid} behavior weights: {weights['intent_bias']}")

    return controller

def post_simulation_pipeline(session_id, agents):
    print("\n[ORCHESTRATION] Running post-simulation analysis...")
    for aid in agents:
        desc, _ = summarize_behavior_from_log(session_id, aid)
        if desc:
            mutate_agent_traits(aid, desc)
            promote_agent_if_eligible(aid)
            score_agent_performance(session_id, aid)
            synthesize_agent_identity(aid)
            build_memory_thread(aid)

def load_prompt(prompt_path):
    with open(prompt_path, 'r') as f:
        try:
            prompt_json = json.load(f)
            return prompt_json.get("starting_prompt", "DEFAULT_PROMPT")
        except:
            return f.read().strip()

# Example:
# session_id = "arena_zenith_v9"
# agents = ["zenith", "aurora", "orion"]
# prompt_file = "../../conversation/prompts/dlg_social_ethics_001.dlg"
# controller = prepare_simulation(session_id, agents, prompt_file)
# controller.start_conversation()
# post_simulation_pipeline(session_id, agents)