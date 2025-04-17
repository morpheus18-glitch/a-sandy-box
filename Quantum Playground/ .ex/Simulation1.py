from backend.conversation.conversation_controller import ConversationArena
from backend.conversation.conversation_controller_panel import ConversationControlPanel

arena = ConversationArena(
    agent_ids=["zenith", "aurora", "orion"],
    prompt_file="../../conversation/prompts/dlg_social_ethics_001.dlg"
)

arena.start_conversation()

# Launch control panel after or during the session
panel = ConversationControlPanel(arena)
panel.command_loop()