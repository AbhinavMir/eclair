import os

def sol_to_json(folder_path, delimiter='\n'):
    file_paths = []
    artifacts_path = os.path.join("artifacts/contracts", folder_path)
    for root, dirs, files in os.walk(artifacts_path):
        for file in files:
            if file.endswith(".json") and not file.endswith("dbg.json"):
                file_paths.append(os.path.abspath(os.path.join(root, file)))
    return delimiter.join(file_paths)
