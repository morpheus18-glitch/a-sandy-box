import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

def visualize_timeline(session_id, agent_id, output_dir="../../visuals/graphs/"):
    path = Path(f"../../conversation/logs/{session_id}_{agent_id}.timeline")
    if not path.exists():
        print(f"[VISUALIZER] Timeline missing: {path}")
        return

    with open(path, 'r') as f:
        timeline = json.load(f)

    times = list(range(len(timeline)))
    intents = [entry.get("intent", "unknown") for entry in timeline]
    sentiments = [entry.get("sentiment", 0.0) for entry in timeline]
    poses = [entry.get("animation_state", {}).get("pose", "idle") for entry in timeline]
    emotions = [entry.get("expression_state", {}).get("expression", "neutral") for entry in timeline]

    fig, ax1 = plt.subplots(figsize=(14, 6))
    ax2 = ax1.twinx()

    # Plot sentiment
    ax1.plot(times, sentiments, label="Sentiment", color="steelblue", linewidth=2)
    ax1.axhline(y=0, color='gray', linestyle='--', linewidth=0.5)
    ax1.set_ylabel("Sentiment Polarity", color="steelblue")

    # Plot intents as scatter with emotion color
    emotion_colors = {
        "joy": "gold", "anger": "red", "sad": "blue", "curious": "purple", "neutral": "gray"
    }

    scatter_colors = [emotion_colors.get(e, "black") for e in emotions]
    ax2.scatter(times, [1.0]*len(times), c=scatter_colors, s=100, label="Intent Markers", alpha=0.6)
    ax2.set_yticks([])
    ax2.set_ylabel("Intent Timeline")

    # Add annotations for pose + intent
    for i, (intent, pose) in enumerate(zip(intents, poses)):
        ax2.annotate(f"{intent}\n{pose}", (i, 1.0), textcoords="offset points", xytext=(0,10),
                     ha='center', fontsize=8, alpha=0.7)

    plt.title(f"Timeline Map: {agent_id} @ {session_id}")
    plt.xlabel("Message Turn Index")
    plt.grid(True)

    # Legend for emotion colors
    patches = [mpatches.Patch(color=c, label=e) for e, c in emotion_colors.items()]
    plt.legend(handles=patches, loc='lower left')

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    output_path = Path(output_dir) / f"{agent_id}_{session_id}_timeline_map.png"
    plt.savefig(output_path)
    plt.close()

    print(f"[VISUALIZER] Saved timeline visualization: {output_path}")