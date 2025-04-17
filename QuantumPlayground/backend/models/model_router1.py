import json
from pathlib import Path
from backend.models.providers import gpt_adapter, claude_adapter, local_stub_adapter

MODEL_ADAPTERS = {
    "gpt-4o": gpt_adapter.call,
    "gpt-4": gpt_adapter.call,
    "claude-3-sonnet": claude_adapter.call,
    "local-stub": local_stub_adapter.call
}

def load_model_binding(agent_id):
    """
    Reads the agent's assigned model from their MCP file.
    """
    path = Path(f"../../protocols/mcp/{agent_id}.mcp")
    if not path.exists():
        print(f"[MODEL_ROUTER] No MCP file for: {agent_id}")
        return "local-stub"

    with open(path, 'r') as f:
        mcp = json.load(f)

    return mcp.get("model_id", "local-stub")

def route_message(msg):
    """
    Unified router interface: Given a message dict, routes it to the correct model backend.
    """
    agent_id = msg.get("from_agent")
    model = load_model_binding(agent_id)
    adapter = MODEL_ADAPTERS.get(model)

    if not adapter:
        print(f"[MODEL_ROUTER] No adapter for model: {model}. Falling back to local-stub.")
        adapter = local_stub_adapter.call

    reply = adapter(msg)
    return reply