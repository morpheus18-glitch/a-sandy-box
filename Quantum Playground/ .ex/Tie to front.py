from mode_manager import detect_conflicting_restrictions

conflicts = detect_conflicting_restrictions()
for category, agents in conflicts.items():
    print(f"[WARNING] Category '{category}' is set to 'none' for agents: {agents}")
    print("Would you like to apply this to ALL agents?")