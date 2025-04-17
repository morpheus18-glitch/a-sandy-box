import json
import os
from pathlib import Path
import openai

MEMORY_DIR = Path("../../agents/memory/")
LOG_DIR = Path("../../conversation/logs/")

def embed_and_store_memory(agent_id, session_id):
    timeline_file = LOG_DIR / f"{session_id}_{agent_id}.timeline"
    memory_file = MEMORY_DIR / f"{agent_id}_memory.json"

    if not timeline_file.exists():
        raise FileNotFoundError(f"No timeline found for {agent_id} @ {session_id}")

    with open(timeline_file, 'r') as f:
        timeline = json.load(f)

    entries_to_store = []

    for entry in timeline:
        text = entry["message"]
        embedding = embed_text(text)
        memory_entry = {
            "turn": entry["turn"],
            "message": text,
            "intent": entry["intent"],
            "emotion": entry["emotion"],
            "tone": entry["tone"],
            "embedding": embedding
        }
        entries_to_store.append(memory_entry)

    MEMORY_DIR.mkdir(parents=True, exist_ok=True)

    # Append to existing memory
    if memory_file.exists():
        existing = json.load(open(memory_file, 'r'))
    else:
        existing = []

    updated_memory = existing + entries_to_store
    json.dump(updated_memory, open(memory_file, 'w'), indent=2)
    print(f"[MEMORY] Stored {len(entries_to_store)} entries to {memory_file}")

def embed_text(text):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response["data"][0]["embedding"]