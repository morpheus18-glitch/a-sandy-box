import time
import random
from backend.models.model_router import route_message
from backend.memory.memory_threading_engine import build_memory_thread
from backend.agents.trait_mutation_engine import mutate_agent_traits
from backend.engine.live_animation_sync_hook import inject_animation_state
from backend.export.live_stream_sim_output import stream_animation_output
from backend.logging.pose_recorder import PoseRecorder
from backend.runtime.live_metrics_engine import LiveMetricsEngine

class RuntimeLoopManager:
    def __init__(self, session_id, agents, prompt_text, rounds=10):
        self.session_id = session_id
        self.agents = agents
        self.rounds = rounds
        self.prompt_text = prompt_text
        self.memory = {aid: [] for aid in agents}
        self.pose_recorders = {aid: PoseRecorder(session_id, aid) for aid in agents}
        self.metrics = LiveMetricsEngine(agents)

    def start(self):
        print(f"\n[RUNTIME LOOP] Session: {self.session_id}")
        print(f"Agents: {self.agents}\n")

        context = self.prompt_text
        agent_queue = self.agents[:]
        random.shuffle(agent_queue)

        for round_num in range(1, self.rounds + 1):
            print(f"\n=== Round {round_num} ===")
            self.metrics.advance_round()

            for agent_id in agent_queue:
                msg = {
                    "from_agent": agent_id,
                    "message": context,
                    "intent": self.derive_intent(context),
                    "sentiment": self.derive_sentiment(context),
                    "tone": self.derive_tone(context)
                }

                reply = route_message(msg)
                enriched = inject_animation_state(agent_id, msg, self.estimate_traits(agent_id))
                enriched["message"] = reply["reply"]
                enriched["source_model"] = reply["source_model"]

                self.pose_recorders[agent_id].record(enriched)
                stream_animation_output(agent_id, enriched)
                self.memory[agent_id].append(enriched)
                self.metrics.record_message(agent_id, enriched)

                print(f"{agent_id.upper()} ({reply['source_model']}): {reply['reply']}")
                context = reply["reply"]

                time.sleep(0.5)

            self.metrics.detect_dominance()

        for aid in self.agents:
            build_memory_thread(aid)
            mutate_agent_traits(aid, self.aggregate_behaviors(aid))
            self.pose_recorders[aid].save()

        self.metrics.print_summary()
        print("\n[RUNTIME LOOP] Simulation Complete.")

    def derive_intent(self, text):
        keywords = ["I think", "maybe", "we should", "you must"]
        return "challenge" if any(k in text.lower() for k in keywords) else "inform"

    def derive_sentiment(self, text):
        if any(w in text.lower() for w in ["never", "fail", "wrong", "angry"]):
            return -0.5
        elif any(w in text.lower() for w in ["love", "great", "agree", "understand"]):
            return 0.7
        return 0.1

    def derive_tone(self, text):
        return "aggressive" if "!" in text else "neutral"

    def estimate_traits(self, agent_id):
        return {
            "confidence": 0.7 + 0.1 * random.random(),
            "eloquence": 0.6 + 0.2 * random.random(),
            "empathy": 0.5 + 0.1 * random.random(),
            "strategic_thinking": 0.6,
            "leadership": 0.5
        }

    def aggregate_behaviors(self, agent_id):
        return {
            "confidence": 0.01,
            "eloquence": 0.005,
            "strategic_thinking": 0.01
        }

# Example usage:
# rlm = RuntimeLoopManager("arena_test", ["zenith", "aurora"], "Let's explore synthetic consciousness.", 5)
# rlm.start()