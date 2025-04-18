import json
import os
from pathlib import Path
import openai
import numpy as np

MEMORY_DIR = Path("../../agents/memory/")

def retrieve_memory(agent_id, query, top_k=5, similarity_threshold=0.75):
    memory_path = MEMORY_DIR / f"{agent_id}_memory.json"
    if not memory_path.exists():
        return []

    with open(memory_path, 'r') as f:
        memory = json.load(f)

    query_vec = embed_text(query)
    scored = []

    for entry in memory:
        entry_vec = entry.get("embedding")
        if entry_vec:
            score = cosine_similarity(query_vec, entry_vec)
            if score >= similarity_threshold:
                scored.append((score, entry))

    scored.sort(reverse=True, key=lambda x: x[0])
    return [e for _, e in scored[:top_k]]

def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    dot = np.dot(vec1, vec2)
    norm = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    return dot / norm if norm != 0 else 0.0

def embed_text(text):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response["data"][0]["embedding"]