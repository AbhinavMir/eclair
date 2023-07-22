# main.py
import os
import sys
import json
import argparse
from .sol_to_json import sol_to_json
from .get_all_files import get_relative_paths_of_sol_files
from .ABI_class import ContractABI
from .templating_logic import create_class

def read_config(config_file_path):
    try:
        with open(config_file_path) as config_file:
            config = json.load(config_file)
        return config
    except FileNotFoundError:
        raise FileNotFoundError("eclair.config.json not found. Please run `eclair init` to create one.")

def process_files(config=None, output_directory="wrappers"):
    if config is None:
        config = read_config("eclair.config.json")

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
            code_file.write(create_class(abi, config))

def initialize_project():
    directory = input("Where do you want to instantiate the project? (Default: Current directory): ")
    if not directory:
        directory = os.getcwd()

    required_items = ['contracts', 'wrappers', 'tests']

    for item in required_items:
        item_path = os.path.join(directory, item)

        if not os.path.exists(item_path):
            print(f"Creating {item} directory...")
            os.makedirs(item_path)

    print("All required directories have been checked and created if necessary.")

    conf_data = {
        'run_compile': True,
        'constructor_args': [],
        'network_name': 'http://example.com',
        'private_key': 'your_private_key',
        'abi_path': 'path_to_abi_file',
        'from_address': 'your_address',
        'gas': 200000,
        'gas_price': 1000000000,
        'nonce': 0,
        'output_directory': 'wrappers',
    }

    conf_file_path = os.path.join(directory, 'eclair.config.json')

    with open(conf_file_path, 'w') as conf_file:
        json.dump(conf_data, conf_file, indent=4)

    print(f"eclair.config.json created with the following data:")
    print(conf_data)

def process_arguments():
    parser = argparse.ArgumentParser(prog='eclair', description='A tool to create library wrappers for Blockchain Business Logic code.')

    subparsers = parser.add_subparsers(dest='command')
    init_parser = subparsers.add_parser('init', help='Initialize a new project')
    # Add more subparsers for different commands if needed

    args = parser.parse_args()

    if args.command == 'init':
        initialize_project()
    elif args.command == '--help' or args.command == 'help' or args.command == "-h" or args.command == "--h":
        print("Usage: eclair [optional command]")
        print("Commands:")
        print("  wrap\t\t\tWrap all contracts in the contracts directory into Python classes and deployers")
        print("  init\t\t\tInitialize a new project")
        print("  help\t\t\tShow this help message")
    elif args.command == "wrap":
        process_files()
    else:
        print("Usage: eclair [optional command]")
        print("Commands:")
        print("  wrap\t\t\tWrap all contracts in the contracts directory into Python classes and deployers")
        print("  init\t\t\tInitialize a new project")
        print("  help\t\t\tShow this help message")

if __name__ == '__main__':
    sys.exit(process_arguments())
