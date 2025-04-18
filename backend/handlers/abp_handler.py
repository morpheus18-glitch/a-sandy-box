import json
import datetime
from jsonschema import validate, ValidationError

# Load ABP schema
with open('../../protocols/schemas/abp_command.json') as f:
    abp_schema = json.load(f)

def process_abp_command(payload):
    try:
        # Validate payload
        validate(instance=payload, schema=abp_schema)
        
        # Simulated routing
        agent_id = payload["agent_id"]
        gesture = payload["gesture"]
        intensity = payload.get("expression_intensity", 0.5)
        duration = payload.get("duration_ms", 1000)
        
        print(f"[ABP] Agent {agent_id} executes '{gesture}' at intensity {intensity} for {duration}ms.")

        # Log command
        log_entry = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "command": payload
        }
        log_abp_event(log_entry)
        return True

    except ValidationError as e:
        print(f"[ABP-ERROR] Invalid payload: {e.message}")
        return False

def log_abp_event(log_entry):
    log_file = f"../../logs/abp_{log_entry['command']['agent_id']}.log"
    with open(log_file, 'a') as f:
        f.write(json.dumps(log_entry) + "\n")