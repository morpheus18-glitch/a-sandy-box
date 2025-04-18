import openai

# Inject your OpenAI key securely (ideally via env var or vault)
openai.api_key = "YOUR_OPENAI_API_KEY"

def call(msg):
    prompt = msg.get("message", "")
    agent_id = msg.get("from_agent", "unknown")
    model_id = msg.get("model_id", "gpt-4o")  # fallback to GPT-4o

    try:
        response = openai.ChatCompletion.create(
            model=model_id,
            messages=[
                {"role": "system", "content": "You are an intelligent AI agent in a simulation."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=512
        )

        reply = response.choices[0].message["content"]
        confidence = float(response.usage.get("completion_tokens", 0)) / 512

        return {
            "reply": reply.strip(),
            "confidence": round(min(1.0, confidence + 0.3), 3),
            "source_model": model_id
        }

    except Exception as e:
        print(f"[GPT_ADAPTER] Error for agent {agent_id}: {e}")
        return {
            "reply": f"[GPT Fallback] Model error: {e}",
            "confidence": 0.5,
            "source_model": model_id
        }