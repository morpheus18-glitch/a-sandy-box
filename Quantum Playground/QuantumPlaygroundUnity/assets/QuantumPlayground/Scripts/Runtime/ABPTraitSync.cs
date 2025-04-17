using UnityEngine;
using TMPro;
using System.IO;
using Newtonsoft.Json;
using System.Collections.Generic;

public class ABPTraitSync : MonoBehaviour
{
    public string agentID = "zenith";
    public SkinnedMeshRenderer faceRenderer;
    public MaterialShaderController shaderController;
    public TextMeshProUGUI debugText;

    private Dictionary<string, float> traits;

    void Start()
    {
        LoadTraits();
        ApplyTraitsToShader();
    }

    void LoadTraits()
    {
        string path = Path.Combine(Application.streamingAssetsPath, "identity", agentID + "_identity.json");
        if (!File.Exists(path))
        {
            Debug.LogWarning($"Trait file not found for agent: {agentID}");
            return;
        }

        string json = File.ReadAllText(path);
        var identity = JsonConvert.DeserializeObject<AgentIdentity>(json);
        traits = identity.traits;

        if (debugText)
        {
            debugText.text = $"Traits Loaded:\n" + JsonConvert.SerializeObject(traits, Formatting.Indented);
        }
    }

    void ApplyTraitsToShader()
    {
        if (shaderController == null || traits == null) return;

        shaderController.SetShaderTrait("confidence", traits.GetValueOrDefault("confidence", 0.5f));
        shaderController.SetShaderTrait("curiosity", traits.GetValueOrDefault("curiosity", 0.5f));
        shaderController.SetShaderTrait("empathy", traits.GetValueOrDefault("empathy", 0.5f));
        shaderController.SetShaderTrait("leadership", traits.GetValueOrDefault("leadership", 0.5f));
    }

    [System.Serializable]
    public class AgentIdentity
    {
        public string agent_id;
        public Dictionary<string, float> traits;
    }
}