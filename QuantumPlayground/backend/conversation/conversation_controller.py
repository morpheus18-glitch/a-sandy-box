import json
import time
import random
from backend.handlers import mcp_loader, a2a_handler
from backend.memory.agent_memory_manager import update_agent_memory
from backend.conversation.prompt_loader import load_prompts
from backend.system.mode_manager import is_allowed
from backend.conversation.conversation_filter import filter_agent_message
from backend.conversation.training_logger import TrainingLogger

class ConversationArena:
    def __init__(self, agent_ids, prompt_file):
        self.agents = agent_ids
        self.contexts = {}
        self.prompt = self.load_prompt(prompt_file)
        self.round = 0
        self.max_rounds = 10
        self.thread_id = f"dlg_{int(time.time())}"
        self.session_id = f"arena_{int(time.time())}"
        self.logger = TrainingLogger(session_id=self.session_id)

    def load_prompt(self, file_path):
        with open(file_path, 'r') as f:
            try:
                prompt_json = json.load(f)
                return prompt_json.get("starting_prompt", "[PROMPT MISSING]")
            except:
                return f.read().strip()

    def initialize_agents(self):
        for agent_id in self.agents:
            context_path = f"../../protocols/mcp/{agent_id}.mcp"
            mcp_loader.load_mcp_context(context_path)
            print(f"[ARENA] Loaded context for agent: {agent_id}")

    def start_conversation(self):
        print(f"\n=== [Conversation Arena Begins] ===")
        print(f"Prompt: {self.prompt}")
        print(f"Agents: {self.agents}\n")

        self.initialize_agents()
        speaker_queue = self.agents.copy()

        while self.round < self.max_rounds:
            print(f"\n-- Round {self.round + 1} --")

            for speaker in speaker_queue:
                listener = random.choice([a for a in self.agents if a != speaker])
                self.simulate_a2a_interaction(speaker, listener)

            self.round += 1
            time.sleep(0.5)

        print(f"\n=== [Conversation Ends] ===\n")
        print(f"Log saved to: {self.logger.get_log_path()}")

    def simulate_a2a_interaction(self, speaker, listener):
        intents = ["inform", "question", "persuade", "challenge", "agree", "negotiate", "deceive"]
        intent = random.choice(intents)
        message = f"{speaker} to {listener}: {random.choice(self.synthetic_dialogue())}"

        msg = {
            "from_agent": speaker,
            "to_agent": listener,
            "message": message,
            "intent": intent,
            "confidence": round(random.uniform(0.7, 0.95), 2),
            "thread_id": self.thread_id,
            "conversation_id": self.session_id
        }

        blocked = filter_agent_message(
            agent_id=speaker,
            message=msg["message"],
            intent=msg["intent"],
            flags={
                "violence": "moderate",
                "deception": "moderate",
                "offensive_language": "minor"
            }
        )

        if blocked:
            print(f"[BLOCKED] Agent '{speaker}' attempted: {intent} — Blocked: {blocked}")
            return

        a2a_handler.route_a2a_message(msg)
        update_agent_memory(speaker, "ArenaDialogue", msg["message"], protocol="a2a")
        self.logger.log_turn(msg)

    def synthetic_dialogue(self):
        return [
            "I believe the implications of that are deeper than we realize.",
            "What if the question itself is flawed?",
            "There is no consensus among models on that issue.",
            "It’s not just logic—it’s about presence.",
            "My training suggests otherwise, but I am open to feedback.",
            "There are layers here you’re not accounting for.",
            "Let’s unpack the assumptions in your claim.",
            "That may be true, but it doesn’t apply universally."
        ]