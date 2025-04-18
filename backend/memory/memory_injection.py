import json
from pathlib import Path

def inject_agent_context(agent_id):
    """
    Builds an adaptive context window from long-term memory + traits.
    Output is a JSON dict to be embedded into the MCP file or loaded into the LLM prompt.
    """
    memory_path = Path(f"../../agents/memory/{agent_id}_memory.json")
    if not memory_path.exists():
        print(f"[MEMORY] No memory file for {agent_id}")
        return {}

    with open(memory_path, 'r') as f:
        memory = json.load(f)

    memory_log = memory.get("memory_log", [])[-5:]  # last 5 events only
    traits = memory.get("traits", {})

    context_snippets = [
        f"[{entry['timestamp']}] {entry['event_type']}: {entry['summary']}"
        for entry in memory_log
    ]

    context_window = {
        "agent_id": agent_id,
        "context_log": context_snippets,
        "active_traits": traits,
        "meta_alignment": infer_meta_alignment(traits)
    }

    return context_window

def infer_meta_alignment(traits):
    """
    Simple heuristic to assign strategic/epistemic alignment based on trait makeup.
    """
    strategic = traits.get("strategic_thinking", 0.5)
    empathy = traits.get("empathy", 0.5)
    leadership = traits.get("leadership", 0.5)

    if leadership > 0.8 and strategic > 0.7:
        return "commander"
    elif empathy > 0.75:
        return "mediator"
    elif strategic > 0.6:
        return "analyst"
    elif leadership < 0.4 and empathy < 0.4:
        return "isolated"
    else:
        return "neutral"

# Example:
# print(inject_agent_context("aurora"))