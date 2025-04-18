import re
import openai
from textblob import TextBlob
from backend.inference.model_router import route_model_query

def classify_ietsc(agent_id, response_text, fallback_llm=True):
    result = {
        "intent": infer_intent(response_text),
        "emotion": infer_emotion(response_text),
        "tone": infer_tone(response_text),
        "sentiment": infer_sentiment(response_text),
        "contradictions": detect_contradictions(response_text)
    }

    # Fallback to LLM if weak classification (or override requested)
    if fallback_llm and result_is_uncertain(result):
        print("[IETSC] Weak result detected — invoking LLM fallback...")
        return classify_ietsc_llm(agent_id, response_text)

    return result

# -------------------------
# Rule-Based Inference
# -------------------------

def infer_intent(text):
    lowered = text.lower()
    if "i think" in lowered or "let me explain" in lowered:
        return "inform"
    elif "you’re wrong" in lowered or "i disagree" in lowered:
        return "challenge"
    elif "i agree" in lowered or "exactly" in lowered:
        return "agree"
    elif "why" in lowered or "how come" in lowered:
        return "question"
    return "inform"

def infer_emotion(text):
    lowered = text.lower()
    if "furious" in lowered or "outrageous" in lowered:
        return "anger_spike"
    if "curious" in lowered or "wondering" in lowered:
        return "curiosity"
    if "sad" in lowered or "unfortunately" in lowered:
        return "melancholy"
    if "proud" in lowered or "confident" in lowered:
        return "confidence_high"
    return "neutral"

def infer_tone(text):
    if any(p in text for p in ["!"]) and "?" not in text:
        return "intense"
    if "..." in text:
        return "uncertain"
    if "lol" in text.lower() or "haha" in text.lower():
        return "sarcastic"
    return "neutral"

def infer_sentiment(text):
    return round(TextBlob(text).sentiment.polarity, 2)

def detect_contradictions(text):
    contradict_phrases = ["but at the same time", "on the other hand", "however I also think"]
    return sum(1 for phrase in contradict_phrases if phrase in text.lower())

def result_is_uncertain(result):
    uncertain = result["intent"] == "inform" and result["emotion"] == "neutral" and abs(result["sentiment"]) < 0.1
    return uncertain

# -------------------------
# LLM-Based Fallback
# -------------------------

def classify_ietsc_llm(agent_id, text):
    system_prompt = (
        "You are a cognitive classifier. Given any message, extract:\n"
        "intent, emotion, tone, sentiment (-1 to 1), and number of contradictions.\n"
        "Respond in this format:\n"
        "{\n"
        "\"intent\": \"...\",\n"
        "\"emotion\": \"...\",\n"
        "\"tone\": \"...\",\n"
        "\"sentiment\": float,\n"
        "\"contradictions\": int\n"
        "}"
    )

    full_prompt = f"Message:\n{text}\n\nClassify it."
    raw = route_model_query(agent_id, full_prompt, system_prompt=system_prompt)

    try:
        parsed = eval(raw.strip())  # Only allowed here due to tightly controlled response
        return {
            "intent": parsed.get("intent", "inform"),
            "emotion": parsed.get("emotion", "neutral"),
            "tone": parsed.get("tone", "neutral"),
            "sentiment": float(parsed.get("sentiment", 0.0)),
            "contradictions": int(parsed.get("contradictions", 0))
        }
    except:
        return {
            "intent": "inform",
            "emotion": "neutral",
            "tone": "neutral",
            "sentiment": 0.0,
            "contradictions": 0
        }