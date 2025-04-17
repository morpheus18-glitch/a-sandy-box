import openai
import json
import os
from pathlib import Path
from backend.memory.memory_retrieval_engine import retrieve_memory

def route_model_query(agent_id, prompt, memory=None, system_prompt=None):
    """
    Routes the request using the model defined in the agent's MCP.
    Auto-injects relevant memory from long-term store.
    """

    mcp_path = Path(f"../../protocols/mcp/{agent_id}.mcp")
    if not mcp_path.exists():
        raise FileNotFoundError(f"MCP not found for agent: {agent_id}")

    with open(mcp_path, 'r') as f:
        mcp = json.load(f)

    model = mcp["model"]
    temperature = mcp.get("temperature", 0.7)
    max_tokens = mcp.get("max_tokens", 2048)
    system_prompt = system_prompt or mcp.get("system_prompt", "")

    # Inject memory (semantic recall)
    retrieved = retrieve_memory(agent_id, prompt, top_k=3)
    memory_msgs = [{"role": "assistant", "content": f"[Memory]: {m['message']}"} for m in retrieved]

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    if memory_msgs:
        messages.extend(memory_msgs)

    if memory:
        messages.extend(memory)

    messages.append({"role": "user", "content": prompt})

    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )

    return response.choices[0].message["content"]