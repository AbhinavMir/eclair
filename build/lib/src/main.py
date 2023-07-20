import get_all_files as file_system
import ABI_class as ABI_class
import sol_to_json as sol_to_json
import templating_logic as templating_logic
import os
import json
import sys

class FunctionAggregator:
    def __init__(self):
        self.sample_args = {
            'run_compile': True,
            'constructor_args': [],
            'network_name': 'http://example.com',
            'private_key': 'your_private_key',
            'abi_path': 'path_to_abi_file',
            'from_address': 'your_address',
            'gas': 200000,
            'gas_price': 1000000000,
            'nonce': 0
        }

    def read_config(self, config_file_path):
        try:
            with open(config_file_path) as config_file:
                config = json.load(config_file)
            return config
        except FileNotFoundError:
            print(f"Config file {config_file_path} not found.")
            sys.exit(1)

    def process_files(self):
        if len(sys.argv) > 1:
            file_path = sys.argv[1:]
        else:
            file_path = ["eclair.conf.json"]
        config = self.read_config(file_path[0])

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
        output_directory = config['output_directory']
        os.makedirs(output_directory, exist_ok=True)

        for abi in abis:
            # Write the code in the specified output directory
            code_filepath = os.path.join(output_directory, f"{abi.name}.py")
            with open(code_filepath, "w") as code_file:
                code_file.write(templating_logic.create_class(abi, config))
