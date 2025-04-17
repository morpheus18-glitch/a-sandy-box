from backend.engine.live_animation_sync_hook import inject_animation_state
from backend.export.live_stream_sim_output import stream_animation_output

def process_agent_message(agent_id, raw_msg, traits):
    """
    Take a raw message from an agent and route through visual animation pipeline.
    """
    enriched = inject_animation_state(agent_id, raw_msg, traits)
    stream_animation_output(agent_id, enriched)
    return enriched

def simulate_loop_example():
    agents = {
        "zenith": {"confidence": 0.9, "eloquence": 0.8},
        "orion": {"empathy": 0.7, "strategic_thinking": 0.85}
    }

    messages = [
        {"from_agent": "zenith", "message": "We should proceed.", "intent": "inform", "sentiment": 0.4, "tone": "neutral"},
        {"from_agent": "orion", "message": "I sense hesitation.", "intent": "challenge", "sentiment": -0.2, "tone": "analytical"}
    ]

    for msg in messages:
        agent_id = msg["from_agent"]
        traits = agents[agent_id]
        enriched = process_agent_message(agent_id, msg, traits)
        print(f"[DASHBOARD] {agent_id}: {enriched['expression_state']['expression']} | Pose: {enriched['animation_state']['pose']}")

# Run this to simulate a live loop stream
# simulate_loop_example()