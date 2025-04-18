import json
import time
from pathlib import Path

def read_abp_stream(stream_path):
    """
    Reads an ABP command stream (JSONL format) and simulates routing each command.
    """
    if not Path(stream_path).exists():
        print(f"[ABP-STREAM] File not found: {stream_path}")
        return

    with open(stream_path, 'r') as f:
        for line in f:
            try:
                command = json.loads(line.strip())
                execute_abp_command(command)
                time.sleep(command.get("duration_ms", 500) / 1000.0)
            except json.JSONDecodeError:
                print("[ABP-STREAM] Invalid JSON line detected.")
            except Exception as e:
                print(f"[ABP-STREAM] Error: {str(e)}")

def execute_abp_command(command):
    """
    Simulates execution of a gesture or animation instruction.
    """
    agent = command.get("agent_id", "unknown")
    gesture = command.get("gesture", "undefined")
    intensity = command.get("intensity", 0.5)

    print(f"[ABP-ACT] Agent {agent} performs '{gesture}' with intensity {intensity}.")

# Example Usage:
# read_abp_stream("../../protocols/abp/aurora_113_live.abp")