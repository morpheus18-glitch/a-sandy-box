using System.IO;
using UnityEngine;

public static class ABPFileIO
{
    public static ABPProfile LoadABP(string agentId)
    {
        string path = Path.Combine(Application.streamingAssetsPath, "abp", $"{agentId}.abp");
        if (!File.Exists(path))
        {
            Debug.LogWarning($"[ABP_IO] Missing ABP file: {path}");
            return null;
        }

        string json = File.ReadAllText(path);
        return JsonUtility.FromJson<ABPProfile>(json);
    }

    public static void SaveABP(string agentId, ABPProfile profile)
    {
        string json = JsonUtility.ToJson(profile, true);
        string folder = Path.Combine(Application.streamingAssetsPath, "abp");
        if (!Directory.Exists(folder)) Directory.CreateDirectory(folder);

        string path = Path.Combine(folder, $"{agentId}.abp");
        File.WriteAllText(path, json);
        Debug.Log($"[ABP_IO] ABP file saved: {path}");
    }
}