using System;
using UnityEngine;

[Serializable]
public class AgentVisualConfig
{
    public string agent_id;
    public string species;
    public string bodyType;
    public string heightClass;
    public string skinTone;
    public string hairStyle;
    public string hairColor;
    public string eyeStyle;
    public string eyeColor;

    public OutfitConfig outfit;
    public AccessoryConfig accessories;
    public SpecialTraits traits;
}

[Serializable]
public class OutfitConfig
{
    public string style;
    public string top;
    public string bottom;
    public string shoes;
    public string fullOutfit; // optional
}

[Serializable]
public class AccessoryConfig
{
    public string hat;
    public string glasses;
    public string necklace;
    public string rings;
}

[Serializable]
public class SpecialTraits
{
    public bool nonHumanLimbs;
    public bool extendedTorso;
    public bool hasTail;
    public string voiceModPreset;
}