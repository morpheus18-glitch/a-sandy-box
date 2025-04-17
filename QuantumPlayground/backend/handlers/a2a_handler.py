import json
from pathlib import Path
from jsonschema import validate, ValidationError

# Load A2A schema
with open('../../protocols/schemas/a2a_message.json') as f:
    a2a_schema = json.load(f)

def process_a2a_stream(file_path):
    path = Path(file_path)
    if not path.exists():
        print(f"[A2A] File not found: {file_path}")
        return

    with open(path, 'r') as f:
        for line in f:
            try:
                msg = json.loads(line.strip())
                validate(instance=msg, schema=a2a_schema)
                route_a2a_message(msg)
            except ValidationError as e:
                print(f"[A2A-ERROR] Validation failed: {e.message}")
            except Exception as ex:
                print(f"[A2A-ERROR] {str(ex)}")

def route_a2a_message(msg):
    print(f"[A2A] {msg['from_agent']} → {msg['to_agent']}: \"{msg['message']}\" ({msg['intent']}, {msg.get('confidence', 'N/A')})")