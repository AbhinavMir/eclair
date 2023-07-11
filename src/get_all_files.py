import os

def get_relative_paths_of_sol_files(folder_path):
    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".sol"):
                relative_path = os.path.relpath(os.path.join(root, file), folder_path)
                file_paths.append(relative_path)
    return file_paths
