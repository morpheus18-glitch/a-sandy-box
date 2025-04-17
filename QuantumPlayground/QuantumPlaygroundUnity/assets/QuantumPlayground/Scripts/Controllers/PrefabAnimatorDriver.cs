using UnityEngine;
using System.Collections.Generic;
using System.IO;
using TMPro;

public class PrefabAnimatorDriver : MonoBehaviour
{
    [System.Serializable]
    public class FrameData {
        public int frame;
        public string pose;
        public string gesture;
        public string expression;
        public Dictionary<string, float> blendshapes;
        public string line;
        public string tone;
        public string intent;
        public float sentiment;
    }

    [System.Serializable]
    public class Timeline {
        public List<FrameData> frames;
    }

    public SkinnedMeshRenderer faceRenderer;
    public Animator animator;
    public TextMeshProUGUI subtitleText;
    public string agentID;
    public string sessionID;
    public float frameRate = 1.0f;

    private Timeline timeline;
    private int currentFrame = 0;
    private float timer = 0;

    void Start()
    {
        LoadTimeline();
    }

    void Update()
    {
        if (timeline == null || timeline.frames.Count == 0) return;

        timer += Time.deltaTime;
        if (timer >= 1f / frameRate)
        {
            PlayFrame(currentFrame);
            currentFrame = (currentFrame + 1) % timeline.frames.Count;
            timer = 0;
        }
    }

    void LoadTimeline()
    {
        string path = Path.Combine(Application.streamingAssetsPath, $"{agentID}_{sessionID}_animtrack.json");
        if (File.Exists(path))
        {
            string json = File.ReadAllText(path);
            timeline = new Timeline { frames = new List<FrameData>(JsonHelper.FromJson<FrameData>(json)) };
            Debug.Log($"[Animator] Loaded {timeline.frames.Count} frames for {agentID}");
        }
        else
        {
            Debug.LogError($"[Animator] Timeline file not found: {path}");
        }
    }

    void PlayFrame(int index)
    {
        var frame = timeline.frames[index];

        // Play animation states
        animator.Play(frame.pose);
        animator.SetTrigger(frame.gesture);

        // Apply blendshapes
        foreach (var kv in frame.blendshapes)
        {
            int id = faceRenderer.sharedMesh.GetBlendShapeIndex(kv.Key);
            if (id >= 0)
                faceRenderer.SetBlendShapeWeight(id, kv.Value * 100f);
        }

        // Display subtitle
        if (subtitleText != null)
            subtitleText.text = frame.line;
    }
}