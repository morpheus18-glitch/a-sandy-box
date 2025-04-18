using UnityEngine;
using System.IO;
using System.Collections.Generic;

public class PrefabController : MonoBehaviour
{
    public SkinnedMeshRenderer faceRenderer;
    public Animator animator;
    public string agentID = "zenith";
    public string animationFeedPath = "Assets/StreamingAssets/zenith_animation.json";

    private Dictionary<string, float> blendTargets;

    void Start()
    {
        blendTargets = new Dictionary<string, float>();
        InvokeRepeating("UpdateFromFeed", 0f, 0.2f); // Update 5x/sec
    }

    void UpdateFromFeed()
    {
        if (!File.Exists(animationFeedPath)) return;
        string json = File.ReadAllText(animationFeedPath);
        AnimationPayload payload = JsonUtility.FromJson<AnimationPayload>(json);

        // Trigger animator parameters
        animator.Play(payload.animation_state.pose);
        animator.SetFloat("gestureIntensity", payload.animation_state.intensity == "high" ? 1f : 0.5f);

        // Update blendshapes
        foreach (var kv in payload.expression_state.blendshapes)
        {
            int idx = faceRenderer.sharedMesh.GetBlendShapeIndex(kv.Key);
            if (idx >= 0)
                faceRenderer.SetBlendShapeWeight(idx, kv.Value * 100f); // 0-100%
        }
    }

    [System.Serializable]
    public class AnimationPayload
    {
        public AnimationState animation_state;
        public ExpressionState expression_state;
    }

    [System.Serializable]
    public class AnimationState
    {
        public string pose;
        public string gesture;
        public string intensity;
    }

    [System.Serializable]
    public class ExpressionState
    {
        public string expression;
        public Dictionary<string, float> blendshapes;
        public string eye_gaze;
        public string mouth_motion;
    }
}