from backend.engine.animation_router import resolve_animation
from backend.engine.expression_anim_mapper import map_expression

def inject_animation_state(agent_id, message, traits):
    """
    Adds animation instructions to agent message dictionary.
    """
    intent = message.get("intent", "inform")
    sentiment = message.get("sentiment", 0.0)
    tone = message.get("tone", "neutral")

    anim = resolve_animation(agent_id, intent, traits)
    expr = map_expression(sentiment, tone)

    message["animation_state"] = anim
    message["expression_state"] = expr
    return message

# Example:
# message = {"message": "I see your point.", "intent": "agree", "sentiment": 0.5, "tone": "warm"}
# updated = inject_animation_state("zenith", message, {"confidence": 0.7, "eloquence": 0.9})