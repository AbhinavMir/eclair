import entry as entry_point
import get_all_files as file_system
import ABI_class as ABI_class
import token_deployer as td
import sol_to_json as sol_to_json

folder_path = "contracts"
sol_file_paths = file_system.get_relative_paths_of_sol_files(folder_path)
all_the_files = []
for sol_file_path in sol_file_paths:
    to_add = sol_to_json.sol_to_json(sol_file_path)
    if len(to_add) > 0:
        all_the_files.append(to_add)

print(all_the_files)

for file in all_the_files:
    abi = ABI_class.ContractABI(file)
    print(abi)