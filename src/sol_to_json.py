import os

def sol_to_json(folder_path):
    file_paths = []
    artifacts_path = os.path.join("artifacts/contracts", folder_path)
    for root, dirs, files in os.walk(artifacts_path):
        for file in files:
            if file.endswith(".json") and not file.endswith("dbg.json"):
                file_paths.append(os.path.join(root, file))
    return file_paths
