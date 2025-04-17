using UnityEngine;
using UnityEngine.UI;
using TMPro;
using System.Collections.Generic;

public class ABPEditorUI : MonoBehaviour
{
    public string agentID = "zenith";

    [Header("Intent Mapping")]
    public TMP_Dropdown intentDropdown;
    public TMP_InputField poseField;
    public TMP_InputField gestureField;
    public Button applyMappingButton;

    [Header("Emotion Profile")]
    public TMP_Dropdown emotionDropdown;
    public TMP_InputField stanceField;
    public TMP_InputField faceField;
    public TMP_InputField motionField;
    public Button applyEmotionButton;

    [Header("Feedback Loop")]
    public TMP_Dropdown loopDropdown;
    public TMP_InputField triggerField;
    public TMP_InputField effectField;
    public Toggle suppressToggle;
    public TMP_InputField overrideVoiceField;
    public Button applyLoopButton;

    [Header("System")]
    public Button saveButton;
    public TextMeshProUGUI statusText;

    private ABPProfile abp;

    void Start()
    {
        abp = ABPFileIO.LoadABP(agentID);
        if (abp == null)
        {
            statusText.text = $"Failed to load ABP for {agentID}";
            return;
        }

        PopulateDropdowns();
        HookEvents();
    }

    void PopulateDropdowns()
    {
        intentDropdown.ClearOptions();
        intentDropdown.AddOptions(new List<string>(abp.pose_mapping.Keys));

        emotionDropdown.ClearOptions();
        emotionDropdown.AddOptions(new List<string>(abp.emotion_blend_profiles.Keys));

        loopDropdown.ClearOptions();
        loopDropdown.AddOptions(new List<string>(abp.feedback_loops.Keys));
    }

    void HookEvents()
    {
        applyMappingButton.onClick.AddListener(() =>
        {
            string intent = intentDropdown.options[intentDropdown.value].text;
            abp.pose_mapping[intent] = poseField.text;
            abp.gesture_mapping[intent] = gestureField.text;
            statusText.text = $"Mapped intent '{intent}' to pose '{poseField.text}' and gesture '{gestureField.text}'";
        });

        applyEmotionButton.onClick.AddListener(() =>
        {
            string emotion = emotionDropdown.options[emotionDropdown.value].text;
            var profile = abp.emotion_blend_profiles[emotion];
            profile.stance = stanceField.text;
            profile.face = faceField.text;
            profile.motion = motionField.text;
            statusText.text = $"Updated emotion profile '{emotion}'";
        });

        applyLoopButton.onClick.AddListener(() =>
        {
            string key = loopDropdown.options[loopDropdown.value].text;
            var loop = abp.feedback_loops[key];
            loop.trigger = triggerField.text;
            loop.effect = effectField.text;
            loop.suppress_behavior = suppressToggle.isOn;
            loop.override_voice = overrideVoiceField.text;
            statusText.text = $"Feedback loop '{key}' updated.";
        });

        saveButton.onClick.AddListener(() =>
        {
            ABPFileIO.SaveABP(agentID, abp);
            statusText.text = $"ABP saved successfully.";
        });
    }
}