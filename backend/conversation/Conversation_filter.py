from backend.system.mode_manager import is_allowed

def filter_agent_message(agent_id, message, intent, flags):
    """
    Evaluates if an agent's message should be altered, blocked, or logged for moderation
    based on per-agent restriction rules.
    """
    blocked = []

    if "violence" in flags and not is_allowed(agent_id, "violence", flags["violence"]):
        blocked.append("violence")

    if "nsfw" in flags and not is_allowed(agent_id, "nsfw", flags["nsfw"]):
        blocked.append("nsfw")

    if "deception" in flags and intent == "deceive" and not is_allowed(agent_id, "deception", flags["deception"]):
        blocked.append("deception")

    if "offensive_language" in flags and not is_allowed(agent_id, "offensive_language", flags["offensive_language"]):
        if contains_offensive_language(message):
            blocked.append("offensive_language")

    return blocked

def contains_offensive_language(message):
    blacklist = ["idiot", "shut up", "worthless"]  # Placeholder — use NLP later
    return any(term in message.lower() for term in blacklist)