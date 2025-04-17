def resolve_animation(agent_id, dominant_intent, traits):
    """
    Given an agent's dominant conversational intent and traits,
    determine animation state priority and transition triggers.
    """
    profile = {
        "pose": "idle",
        "transition": "none",
        "gesture": "neutral",
        "intensity": "moderate"
    }

    if dominant_intent == "inform":
        profile["gesture"] = "hand_open"
        profile["pose"] = "explain_stand"

    elif dominant_intent == "challenge":
        profile["gesture"] = "point"
        profile["pose"] = "lean_forward"
        profile["intensity"] = "high"

    elif dominant_intent == "agree":
        profile["gesture"] = "nod"
        profile["pose"] = "open_posture"

    elif dominant_intent == "deceive":
        profile["gesture"] = "glance_away"
        profile["pose"] = "shifty"

    # Trait amplification
    if traits.get("confidence", 0.5) > 0.85:
        profile["intensity"] = "high"
    if traits.get("eloquence", 0.5) > 0.8:
        profile["gesture"] = "smooth_flick"
    if traits.get("empathy", 0.5) > 0.8:
        profile["gesture"] = "gentle_touch"

    return profile

# Example:
# state = resolve_animation("zenith", "challenge", {"confidence": 0.9, "eloquence": 0.7})
# => {pose: "lean_forward", gesture: "point", intensity: "high"}