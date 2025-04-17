import openai
from pathlib import Path
import json
import os

def route_model_query(agent_id, prompt, memory=None, system_prompt=None):
    """
    Routes the request using the model defined in the agent's MCP.
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

    if model.startswith("gpt"):
        return query_openai(prompt, memory, model, temperature, max_tokens, system_prompt)
    
    raise NotImplementedError(f"Model '{model}' not supported yet.")

def query_openai(prompt, memory, model, temperature, max_tokens, system_prompt):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    messages = []

    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    if memory:
        for m in memory:
            messages.append({"role": m["role"], "content": m["content"]})

    messages.append({"role": "user", "content": prompt})

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )

    return response.choices[0].message["content"]