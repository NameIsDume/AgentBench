import json
from collections import defaultdict
import pandas as pd
tasks = defaultdict(dict)

model_files = {
    "qwen2.5:0.5b": "outputs/2025-05-21-17-04-48/qwen2.5:0.5b/os-std/runs.jsonl",
    "qwen2.5:1.5b": "outputs/2025-05-21-17-19-14/qwen2.5:1.5b/os-std/runs.jsonl",
    "qwen2.5-coder:0.5b": "outputs/2025-05-22-14-16-11/qwen2.5-coder:0.5b/os-std/runs.jsonl",
    "qwen2.5-coder:1.5b": "outputs/2025-05-22-14-42-04/qwen2.5-coder:1.5b/os-std/runs.jsonl",
    "qwen3-1.7b": "outputs/2025-05-26-14-40-08/qwen3-1.7b/os-std/runs.jsonl",
    "qwen3-0.6b": "outputs/2025-05-30-09-17-43/qwen3-0.6b/os-std/runs.jsonl",
    "qwen3-0.6b with rig": "outputs/2025-06-05-17-28-40/gpt-3.5-turbo-0613/os-std/runs.jsonl"
}

results = defaultdict(dict)

for model, filepath in model_files.items():
    with open(filepath, "r") as f:
        for line in f:
            try:
                entry = json.loads(line)
                task_id = entry["index"]
                success = entry.get("output", {}).get("result", {}).get("result", None)
                results[task_id][model] = success
            except Exception as e:
                print(f"Erreur sur {model}, ligne ignorée : {e}")

# DataFrame avec True/False/None (succès, échec, non tenté)
df = pd.DataFrame.from_dict(results, orient="index")
df.index.name = "task_id"
df.to_csv("resultats_par_task.csv")

# Affichage simplifié des performances
print("\n✅ Taux de réussite par modèle :")
for model in df.columns:
    total = df[model].notna().sum()
    success = (df[model] == True).sum()
    rate = round(100 * success / total, 2) if total > 0 else 0
    print(f"{model}: {rate}% success")