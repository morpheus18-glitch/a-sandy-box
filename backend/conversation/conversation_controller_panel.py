import os
import json
import random
from backend.conversation.training_logger import TrainingLogger

class ConversationControlPanel:
    def __init__(self, arena_instance):
        self.arena = arena_instance
        self.logger = arena_instance.logger
        self.active = True
        self.injected_turns = 0

    def command_loop(self):
        print("\n[CONTROL PANEL ACTIVE] — type 'help' for commands\n")
        while self.active:
            cmd = input(">>> ").strip().lower()

            if cmd == "pause":
                print("[PANEL] Conversation paused.")
                input("[PANEL] Press Enter to resume...")

            elif cmd == "inject":
                agent = input("Agent to speak: ").strip()
                msg = input("Injected message: ").strip()
                self.injected_turns += 1
                turn = {
                    "from_agent": agent,
                    "message": msg,
                    "intent": "injected",
                    "confidence": 1.0,
                    "turn_id": f"inject_{self.injected_turns}",
                    "conversation_id": self.arena.session_id
                }
                self.logger.log_turn(turn)
                print(f"[PANEL] Injected custom line from {agent}.")

            elif cmd == "log":
                log_path = self.logger.get_log_path()
                print(f"[PANEL] Log path: {log_path}")
                print("[PANEL] Previewing last 3 turns:")
                self.preview_last_log_lines(log_path, 3)

            elif cmd == "agents":
                print("[PANEL] Current agents:")
                for aid in self.arena.agents:
                    print(f" - {aid}")

            elif cmd == "info":
                print(f"Session ID: {self.arena.session_id}")
                print(f"Prompt: {self.arena.prompt}")
                print(f"Rounds Run: {self.arena.round}")

            elif cmd == "exit" or cmd == "quit":
                print("[PANEL] Exiting control panel.")
                self.active = False

            elif cmd == "help":
                self.print_help()

            else:
                print("[PANEL] Unknown command. Type 'help' to view commands.")

    def preview_last_log_lines(self, file_path, n=3):
        if not os.path.exists(file_path):
            print("[PANEL] No log file found.")
            return
        with open(file_path, 'r') as f:
            lines = f.readlines()[-n:]
            for line in lines:
                print(">", line.strip())

    def print_help(self):
        print("""
Available Commands:
  pause         - Pause the conversation loop
  inject        - Inject a custom message from an agent
  log           - Show last few entries in training log
  agents        - List current agents
  info          - Show session metadata
  exit / quit   - Exit control panel
""")