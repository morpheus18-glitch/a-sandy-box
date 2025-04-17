def map_expression(sentiment_score, tone):
    """
    Given sentiment polarity (-1 to 1) and tone tag (e.g., 'aggressive', 'warm'),
    return blendshape targets and facial animation tags.
    """
    profile = {
        "expression": "neutral",
        "blendshapes": {},
        "eye_gaze": "forward",
        "mouth_motion": "default"
    }

    # Sentiment polarity mapping
    if sentiment_score >= 0.7:
        profile["expression"] = "joy"
        profile["blendshapes"] = {"smile": 0.8, "eyebrow_raise": 0.4}
    elif sentiment_score <= -0.5:
        profile["expression"] = "anger" if tone == "aggressive" else "sad"
        profile["blendshapes"] = {"frown": 0.7, "brow_lower": 0.5}
    elif -0.3 < sentiment_score < 0.3:
        profile["expression"] = "neutral"
    else:
        profile["expression"] = "curious"
        profile["blendshapes"] = {"brow_raise": 0.5, "mouth_corner_up": 0.2}

    # Tone mapping modifiers
    if tone == "aggressive":
        profile["eye_gaze"] = "direct"
        profile["mouth_motion"] = "clipped"
    elif tone == "warm":
        profile["eye_gaze"] = "soft"
        profile["mouth_motion"] = "rounded"

    return profile

# Example:
# map_expression(0.85, "warm")
# => expression: joy, smile: 0.8, gaze: soft