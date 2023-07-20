import get_all_files as file_system
import ABI_class as ABI_class
import sol_to_json as sol_to_json
import templating_logic as templating_logic
import os
import sys


def file_exists(filepath):
    return os.path.isfile(filepath)

folder_path = "contracts"
sol_folder_paths = file_system.get_relative_paths_of_sol_files(folder_path)
sol_file_paths = []
temp_list = []
for sol_folder_path in sol_folder_paths:
    current_item = sol_to_json.sol_to_json(sol_folder_path)
    if "\n" in current_item:
        temp_list = current_item.split("\n")
        for item in temp_list:
            sol_file_paths.append(item)
    else:
        sol_file_paths.append(current_item)

abis = []
for sol_file_path in sol_file_paths:
    abis.append(ABI_class.ContractABI(sol_file_path))

# Get the command line argument for the code output directory
output_directory = sys.argv[1] if len(sys.argv) > 1 else "out"
os.makedirs(output_directory, exist_ok=True)

for abi in abis:
    # Write the code in the specified output directory
    code_filepath = os.path.join(output_directory, f"{abi.name}.py")
    with open(code_filepath, "w") as code_file:
        code_file.write(templating_logic.create_class(abi))
