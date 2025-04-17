import json
from pathlib import Path

def generate_agent_protocol_files(agent_template_path):
    with open(agent_template_path, 'r') as f:
        agent = json.load(f)

    mcp = {
        "model_id": agent["llm_model"],
        "agent_id": agent["agent_id"],
        "active_topics": [],
        "context_window": [],
        "role_alignment": agent["archetype"].lower(),
        "context_score": 0.5
    }

    abp = {
        "agent_id": agent["agent_id"],
        "timestamp": "init",
        "gesture": "idle_pose",
        "expression_intensity": 0.3,
        "duration_ms": 500
    }

    mcp_path = f"../../protocols/mcp/{agent['agent_id']}.mcp"
    abp_path = f"../../protocols/abp/{agent['agent_id']}_boot.abp"

    with open(mcp_path, 'w') as f:
        json.dump(mcp, f, indent=2)

    with open(abp_path, 'w') as f:
        json.dump(abp, f, indent=2)

    print(f"[AGENT INIT] Protocol files created for agent {agent['agent_id']}")