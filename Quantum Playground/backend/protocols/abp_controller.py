import json
from pathlib import Path

def load_abp(agent_id):
    path = Path(f"../../protocols/abp/{agent_id}.abp")
    if not path.exists():
        print(f"[ABP] Missing protocol file: {path}")
        return None

    with open(path, 'r') as f:
        return json.load(f)

def resolve_abp_response(abp, ai_state):
    """
    Maps AI cognitive/emotional state into physical behavior tags.
    ai_state = {
        "intent": "challenge",
        "emotion": "confidence_high",
        "traits": {"confidence": 0.9, "empathy": 0.4},
        "contradictions": 1
    }
    """
    behavior = {}

    # Pose & Gesture
    behavior["pose"] = abp["pose_mapping"].get(ai_state["intent"], "idle")
    behavior["gesture"] = abp["gesture_mapping"].get(ai_state.get("tone", "neutral"), "hand_rest")

    # Emotion profile
    if ai_state.get("emotion") in abp["emotion_blend_profiles"]:
        behavior.update(abp["emotion_blend_profiles"][ai_state["emotion"]])

    # Feedback loop
    if ai_state.get("contradictions", 0) > 3:
        glitch = abp["feedback_loops"].get("sync_loss")
        if glitch:
            behavior["pose"] = glitch["effect"]
            if glitch["override_voice"]:
                behavior["voice"] = glitch["override_voice"]

    return behavior

# Example usage:
# abp = load_abp("zenith")
# ai_state = {"intent": "challenge", "emotion": "confidence_high", "traits": {...}}
# resolved = resolve_abp_response(abp, ai_state)