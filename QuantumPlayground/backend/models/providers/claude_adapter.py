import anthropic

client = anthropic.Anthropic(
    api_key="YOUR_ANTHROPIC_API_KEY"
)

def call(msg):
    prompt = msg.get("message", "")
    agent_id = msg.get("from_agent", "unknown")
    model_id = msg.get("model_id", "claude-3-sonnet-20240229")  # Claude 3 default

    try:
        response = client.messages.create(
            model=model_id,
            max_tokens=512,
            temperature=0.7,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        reply = response.content[0].text.strip()

        return {
            "reply": reply,
            "confidence": 0.88,  # Static for now; can tune based on metadata later
            "source_model": model_id
        }

    except Exception as e:
        print(f"[CLAUDE_ADAPTER] Error for agent {agent_id}: {e}")
        return {
            "reply": f"[Claude Fallback] Model error: {e}",
            "confidence": 0.5,
            "source_model": model_id
        }