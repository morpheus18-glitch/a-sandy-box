using System;
using System.Collections.Generic;
using UnityEngine;

[Serializable]
public class ABPProfile
{
    public string agent_id;
    public string version;
    public Dictionary<string, string> pose_mapping;
    public Dictionary<string, string> gesture_mapping;
    public Dictionary<string, ABPEmotionBlend> emotion_blend_profiles;
    public Dictionary<string, ABPFeedbackLoop> feedback_loops;
    public ABPTrainingMode training_mode;
}

[Serializable]
public class ABPEmotionBlend
{
    public string stance;
    public string speed;
    public string face;
    public string gaze;
    public string hands;
    public string motion;
    public string voice;
    public string gesture;
}

[Serializable]
public class ABPFeedbackLoop
{
    public string trigger;
    public string effect;
    public bool suppress_behavior;
    public string override_voice;
}

[Serializable]
public class ABPTrainingMode
{
    public bool enabled;
    public string reward_style;
    public string evolution_trait;
}