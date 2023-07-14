import get_all_files as file_system, ABI_class as ABI_class, sol_to_json as sol_to_json

folder_path = "contracts"
sol_file_paths = file_system.get_relative_paths_of_sol_files(folder_path)
all_the_files = [sol_to_json.sol_to_json(sol_file_path) for sol_file_path in sol_file_paths if sol_to_json.sol_to_json(sol_file_path)]
abi_classes = [ABI_class.ContractABI(file) for file in all_the_files]

for abi in abi_classes:
    print(abi)