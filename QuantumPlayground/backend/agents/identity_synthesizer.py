import json
from pathlib import Path
from statistics import mean

def synthesize_agent_identity(agent_id):
    memory_path = Path(f"../../agents/memory/{agent_id}_memory.json")
    if not memory_path.exists():
        print(f"[IDENTITY] Memory not found for {agent_id}")
        return

    with open(memory_path, 'r') as f:
        memory = json.load(f)

    traits = memory.get("traits", {})
    sessions = memory.get("session_thread", [])

    identity = {
        "agent_id": agent_id,
        "core_traits": {},
        "dominant_intents": {},
        "conversation_style": "",
        "behavioral_signature": "",
        "summary": ""
    }

    identity["core_traits"] = {k: round(v, 2) for k, v in traits.items()}

    intent_totals = {}
    for s in sessions:
        session_id = s["session_id"]
        analysis_path = Path(f"../../conversation/logs/{session_id}.analysis")
        if not analysis_path.exists():
            continue
        with open(analysis_path, 'r') as f:
            analysis = json.load(f)
            intents = analysis.get("dominant_intents", {}).get(agent_id, {})
            for k, v in intents.items():
                intent_totals[k] = intent_totals.get(k, 0) + v

    total_intents = sum(intent_totals.values())
    if total_intents > 0:
        identity["dominant_intents"] = {
            k: round(v / total_intents, 2) for k, v in intent_totals.items()
        }

    # Style synthesis
    identity["conversation_style"] = determine_style(identity["core_traits"])
    identity["behavioral_signature"] = generate_signature(intent_totals, traits)
    identity["summary"] = generate_summary(identity)

    print(f"[IDENTITY] Synthesized identity for {agent_id}")
    return identity

def determine_style(traits):
    if traits.get("eloquence", 0.5) > 0.8:
        return "articulate & reflective"
    elif traits.get("confidence", 0.5) > 0.85:
        return "assertive & direct"
    elif traits.get("empathy", 0.5) > 0.75:
        return "warm & collaborative"
    return "adaptive generalist"

def generate_signature(intents, traits):
    high = max(intents, key=intents.get) if intents else "inform"
    if traits.get("strategic_thinking", 0.5) > 0.7:
        return f"{high}-oriented, with analytical undertones"
    if traits.get("empathy", 0.5) > 0.7:
        return f"{high}-driven, with emotional resonance"
    return f"{high}-balanced"

def generate_summary(identity):
    trait = identity["core_traits"]
    tone = identity["conversation_style"]
    sig = identity["behavioral_signature"]
    return (
        f"{identity['agent_id']} is primarily {tone}, shaped by dominant traits like "
        f"confidence ({trait.get('confidence')}), empathy ({trait.get('empathy')}), "
        f"and strategic thinking ({trait.get('strategic_thinking')}). The agent’s behavioral pattern is "
        f"{sig}."
    )

# Example:
# identity = synthesize_agent_identity("aurora")
# print(json.dumps(identity, indent=2))