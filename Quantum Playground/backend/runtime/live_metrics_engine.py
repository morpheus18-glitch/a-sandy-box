from collections import defaultdict
import numpy as np

class LiveMetricsEngine:
    def __init__(self, agent_ids):
        self.agent_ids = agent_ids
        self.metrics = {aid: self._init_agent() for aid in agent_ids}
        self.round = 0
        self.timeline = defaultdict(list)

    def _init_agent(self):
        return {
            "messages": 0,
            "interrupts": 0,
            "dominance_score": 0.0,
            "emotional_variance": [],
            "intent_counts": defaultdict(int)
        }

    def record_message(self, agent_id, msg):
        self.metrics[agent_id]["messages"] += 1
        self.metrics[agent_id]["intent_counts"][msg.get("intent", "unknown")] += 1
        self.metrics[agent_id]["emotional_variance"].append(msg.get("sentiment", 0.0))
        self.timeline[self.round].append(agent_id)

    def detect_dominance(self):
        last_agents = self.timeline[self.round]
        for agent_id in self.agent_ids:
            if last_agents.count(agent_id) > 1:
                self.metrics[agent_id]["interrupts"] += 1
                self.metrics[agent_id]["dominance_score"] += 0.1

    def advance_round(self):
        self.round += 1
        self.timeline[self.round] = []

    def summarize(self):
        summary = {}
        for aid in self.agent_ids:
            m = self.metrics[aid]
            emotional_variance = np.std(m["emotional_variance"]) if m["emotional_variance"] else 0.0
            summary[aid] = {
                "messages": m["messages"],
                "dominance": round(m["dominance_score"], 2),
                "volatility": round(emotional_variance, 3),
                "interrupts": m["interrupts"],
                "intent_distribution": dict(m["intent_counts"])
            }
        return summary

    def print_summary(self):
        print("\n[METRICS] Live Agent Behavior Summary")
        summary = self.summarize()
        for aid, stats in summary.items():
            print(f" - {aid.upper()}: {stats}")