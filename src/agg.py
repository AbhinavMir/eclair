import os
import json
from .get_all_files import get_relative_paths_of_sol_files
from .ABI_class import ContractABI
from .sol_to_json import sol_to_json
from .templating_logic import create_class

class FunctionAggregator:
    def __init__(self, config_file_path="eclair.config.json"):
        self.args = self.read_config(config_file_path)

    def read_config(self, config_file_path):
        try:
            with open(config_file_path) as config_file:
                config = json.load(config_file)
            return config
        except FileNotFoundError:
            raise FileNotFoundError("eclair.config.json not found. Please run `eclair init` to create one.")
    
    def process_files(self, config=None, output_directory="wrappers"):
        if config is None:
            config = self.read_config("eclair.config.json")

        folder_path = "contracts"
        sol_folder_paths = get_relative_paths_of_sol_files(folder_path)
        sol_file_paths = []
        for sol_folder_path in sol_folder_paths:
            current_item = sol_to_json(sol_folder_path)
            if "\n" in current_item:
                sol_file_paths.extend(current_item.split("\n"))
            else:
                sol_file_paths.append(current_item)

        abis = [ContractABI(sol_file_path) for sol_file_path in sol_file_paths]

        os.makedirs(output_directory, exist_ok=True)

        for abi in abis:
            # Write the code in the specified output directory
            code_filepath = os.path.join(output_directory, f"{abi.name}.py")
            with open(code_filepath, "w") as code_file:
                print(f"Writing {abi.name}.py...")
                code_file.write(create_class(abi, config))
