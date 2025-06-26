# import json
# import os
# import pandas as pd
# from collections import defaultdict

# # Dictionnaire des modèles et chemins de fichiers
# model_files = {
#     "qwen2.5:0.5b": "outputs/2025-05-21-17-04-48/qwen2.5:0.5b/os-std/runs.jsonl",
#     "qwen2.5:1.5b": "outputs/2025-05-21-17-19-14/qwen2.5:1.5b/os-std/runs.jsonl",
#     "qwen2.5-coder:0.5b": "outputs/2025-05-22-14-16-11/qwen2.5-coder:0.5b/os-std/runs.jsonl",
#     "qwen2.5-coder:1.5b": "outputs/2025-05-22-14-42-04/qwen2.5-coder:1.5b/os-std/runs.jsonl",
#     "qwen3-1.7b": "outputs/2025-05-26-14-40-08/qwen3-1.7b/os-std/runs.jsonl",
#     "qwen3-0.6b": "outputs/2025-05-30-09-17-43/qwen3-0.6b/os-std/runs.jsonl",
# }

# # Conteneur pour les résultats
# results = []

# for model_name, path in model_files.items():
#     if not os.path.isfile(path):
#         continue

#     success_count = 0
#     failure_counters = defaultdict(int)

#     with open(path, "r") as f:
#         for line in f:
#             try:
#                 entry = json.loads(line.strip())
#                 output = entry.get("output", {})
#                 result = output.get("result", {}).get("result")
#                 status = output.get("status", "unknown")
#                 history = output.get("history", [])
#                 last_agent = next((s["content"] for s in reversed(history) if s.get("role") == "agent"), "")

#                 if result is True:
#                     success_count += 1
#                 else:
#                     if "Act: finish" in last_agent:
#                         failure_counters["gave_up"] += 1
#                     elif "Act: answer" in last_agent:
#                         failure_counters["incorrect_answer"] += 1
#                     else:
#                         failure_counters[status] += 1

#             except json.JSONDecodeError:
#                 continue

#     results.append({"llm": model_name, "result": "success", "reason": "", "count": success_count})
#     for reason, count in failure_counters.items():
#         results.append({"llm": model_name, "result": "failure", "reason": reason, "count": count})

# # Création du DataFrame final
# df = pd.DataFrame(results)
# print(df)
# invalids = []

import json
import os
import pandas as pd
from collections import defaultdict

# Dictionnaire des modèles et chemins de fichiers
model_files = {
    "qwen2.5:0.5b": "outputs/2025-05-21-17-04-48/qwen2.5:0.5b/os-std/runs.jsonl",
    "qwen2.5:1.5b": "outputs/2025-05-21-17-19-14/qwen2.5:1.5b/os-std/runs.jsonl",
    "qwen2.5-coder:0.5b": "outputs/2025-05-22-14-16-11/qwen2.5-coder:0.5b/os-std/runs.jsonl",
    "qwen2.5-coder:1.5b": "outputs/2025-05-22-14-42-04/qwen2.5-coder:1.5b/os-std/runs.jsonl",
    "qwen3-1.7b": "outputs/2025-05-26-14-40-08/qwen3-1.7b/os-std/runs.jsonl",
    "qwen3-0.6b": "outputs/2025-05-30-09-17-43/qwen3-0.6b/os-std/runs.jsonl",
    "qwen3-0.6b with rig": "outputs/2025-06-05-17-28-40/gpt-3.5-turbo-0613/os-std/runs.jsonl"
}

results = []
invalids = []

for model_name, path in model_files.items():
    if not os.path.isfile(path):
        print(f"File not found: {path}")
        continue

    success_count = 0
    failure_counters = defaultdict(int)

    with open(path, "r") as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                output = entry.get("output", {})
                result = output.get("result", {}).get("result")
                status = output.get("status", "unknown")
                history = output.get("history", [])
                last_agent = next((s["content"] for s in reversed(history) if s.get("role") == "agent"), "")

                if result is True:
                    success_count += 1
                else:
                    if "Act: finish" in last_agent:
                        failure_counters["gave_up"] += 1
                    elif "Act: answer" in last_agent:
                        failure_counters["incorrect_answer"] += 1
                    else:
                        failure_counters[status] += 1

                    if status == "agent invalid action":
                        invalids.append({
                            "model": model_name,
                            "invalid_action": last_agent
                        })

            except json.JSONDecodeError:
                continue

    results.append({"llm": model_name, "result": "success", "reason": "", "count": success_count})
    for reason, count in failure_counters.items():
        results.append({"llm": model_name, "result": "failure", "reason": reason, "count": count})

# Affichage des résultats
df = pd.DataFrame(results)
print(df)

print(f"\nFound {len(invalids)} invalid actions")
if invalids:
    print(f"\nExample from {invalids[0]['model']}:\n")
    print(invalids[0]["invalid_action"])
