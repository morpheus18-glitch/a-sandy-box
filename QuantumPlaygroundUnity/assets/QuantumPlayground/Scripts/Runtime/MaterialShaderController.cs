using UnityEngine;

public class MaterialShaderController : MonoBehaviour
{
    public Material targetMaterial;

    public void SetShaderTrait(string traitName, float value)
    {
        if (targetMaterial == null) return;

        string shaderParam = $"_Trait_{traitName}";
        targetMaterial.SetFloat(shaderParam, value);
    }
}