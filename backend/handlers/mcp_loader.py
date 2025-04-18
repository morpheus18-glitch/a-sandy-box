import json
from jsonschema import validate, ValidationError
from pathlib import Path

# Load MCP schema
with open('../../protocols/schemas/mcp_context.json') as f:
    mcp_schema = json.load(f)

def load_mcp_context(file_path):
    """
    Load and validate an .mcp file, then simulate applying context.
    """
    path = Path(file_path)
    if not path.exists():
        print(f"[MCP] Context file not found: {file_path}")
        return

    with open(path, 'r') as f:
        context = json.load(f)
    
    try:
        validate(instance=context, schema=mcp_schema)
        apply_context(context)
    except ValidationError as e:
        print(f"[MCP-ERROR] Schema validation failed: {e.message}")
    except Exception as ex:
        print(f"[MCP-ERROR] Unexpected error: {str(ex)}")

def apply_context(context):
    model_id = context.get("model_id")
    agent_id = context.get("agent_id")
    topics = context.get("active_topics", [])
    role = context.get("role_alignment", "neutral")
    print(f"[MCP] Loaded context for agent '{agent_id}' (Model: {model_id})")
    print(f"   Active Topics: {topics}")
    print(f"   Role Alignment: {role}")
    # This is where live memory injection or role tuning would occur

# Example:
# load_mcp_context("../../protocols/mcp/example.mcp")