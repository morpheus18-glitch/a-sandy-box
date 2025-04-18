using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class AgentVisualEditorUI : MonoBehaviour
{
    public string agentID = "zenith";

    [Header("Base Appearance")]
    public TMP_Dropdown speciesDropdown;
    public TMP_Dropdown bodyDropdown;
    public TMP_Dropdown heightDropdown;
    public TMP_Dropdown skinDropdown;

    public TMP_Dropdown hairStyleDropdown;
    public TMP_InputField hairColorInput;
    public TMP_Dropdown eyeStyleDropdown;
    public TMP_InputField eyeColorInput;

    [Header("Outfit")]
    public TMP_Dropdown outfitStyleDropdown;
    public TMP_InputField topInput;
    public TMP_InputField bottomInput;
    public TMP_InputField shoesInput;

    [Header("Accessories")]
    public TMP_InputField hatInput;
    public TMP_InputField glassesInput;
    public TMP_InputField necklaceInput;
    public TMP_InputField ringsInput;

    [Header("Special Traits")]
    public Toggle tailToggle;
    public Toggle limbToggle;
    public Toggle torsoToggle;
    public TMP_Dropdown voiceDropdown;

    [Header("System")]
    public Button saveButton;
    public TextMeshProUGUI statusText;

    private AgentVisualConfig config;

    void Start()
    {
        LoadDefaults();
        HookEvents();
    }

    void LoadDefaults()
    {
        config = new AgentVisualConfig();
        config.agent_id = agentID;
        config.species = "human";
        config.heightClass = "average";
        config.outfit = new OutfitConfig();
        config.accessories = new AccessoryConfig();
        config.traits = new SpecialTraits();
        statusText.text = $"Ready to configure: {agentID}";
    }

    void HookEvents()
    {
        saveButton.onClick.AddListener(() =>
        {
            config.species = speciesDropdown.options[speciesDropdown.value].text;
            config.bodyType = bodyDropdown.options[bodyDropdown.value].text;
            config.heightClass = heightDropdown.options[heightDropdown.value].text;
            config.skinTone = skinDropdown.options[skinDropdown.value].text;

            config.hairStyle = hairStyleDropdown.options[hairStyleDropdown.value].text;
            config.hairColor = hairColorInput.text;
            config.eyeStyle = eyeStyleDropdown.options[eyeStyleDropdown.value].text;
            config.eyeColor = eyeColorInput.text;

            config.outfit.style = outfitStyleDropdown.options[outfitStyleDropdown.value].text;
            config.outfit.top = topInput.text;
            config.outfit.bottom = bottomInput.text;
            config.outfit.shoes = shoesInput.text;

            config.accessories.hat = hatInput.text;
            config.accessories.glasses = glassesInput.text;
            config.accessories.necklace = necklaceInput.text;
            config.accessories.rings = ringsInput.text;

            config.traits.hasTail = tailToggle.isOn;
            config.traits.nonHumanLimbs = limbToggle.isOn;
            config.traits.extendedTorso = torsoToggle.isOn;
            config.traits.voiceModPreset = voiceDropdown.options[voiceDropdown.value].text;

            SaveVisualConfig();
        });
    }

    void SaveVisualConfig()
    {
        string json = JsonUtility.ToJson(config, true);
        string folder = System.IO.Path.Combine(Application.streamingAssetsPath, "visuals");
        if (!System.IO.Directory.Exists(folder)) System.IO.Directory.CreateDirectory(folder);

        string path = System.IO.Path.Combine(folder, $"{agentID}_visual.json");
        System.IO.File.WriteAllText(path, json);
        statusText.text = $"Saved config: {path}";
    }
}