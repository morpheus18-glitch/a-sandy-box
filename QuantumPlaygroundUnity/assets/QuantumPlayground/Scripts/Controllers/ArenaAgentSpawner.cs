using UnityEngine;
using System.Collections.Generic;

public class ArenaAgentSpawner : MonoBehaviour
{
    [System.Serializable]
    public class AgentSpawnConfig
    {
        public string agentID;
        public string sessionID;
        public GameObject prefab;
        public Vector3 spawnPosition;
        public Vector3 rotation;
    }

    public List<AgentSpawnConfig> agentsToSpawn;

    void Start()
    {
        foreach (var agent in agentsToSpawn)
        {
            GameObject go = Instantiate(agent.prefab, agent.spawnPosition, Quaternion.Euler(agent.rotation));
            go.name = $"Agent_{agent.agentID}";

            var animDriver = go.GetComponent<PrefabAnimatorDriver>();
            if (animDriver != null)
            {
                animDriver.agentID = agent.agentID;
                animDriver.sessionID = agent.sessionID;
                animDriver.frameRate = 1.0f;
            }
            else
            {
                Debug.LogWarning($"[Spawner] Missing animator driver on prefab: {agent.prefab.name}");
            }
        }

        Debug.Log($"[Spawner] Spawned {agentsToSpawn.Count} agents.");
    }
}