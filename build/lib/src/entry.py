import os
import json

class ProjectInitializer:
    def __init__(self):
        self.directory = None
        self.rpc_endpoint = None
        self.deployer_address = None
    
    def get_user_input(self):
        self.directory = input("Where do you want to instantiate the project? (Default: Current directory): ")
        if not self.directory:
            self.directory = os.getcwd()
        
        self.rpc_endpoint = input("Preferred RPC endpoint (Default: localhost:7545): ")
        if not self.rpc_endpoint:
            self.rpc_endpoint = "localhost:7545"
        
        self.deployer_address = input("Preferred Deployer address: ")
    
    def check_and_create_directories(self):
        required_items = ['contracts', 'wrappers', 'tests']

        for item in required_items:
            item_path = os.path.join(self.directory, item)

            if not os.path.exists(item_path):
                print(f"Creating {item} directory...")
                os.makedirs(item_path)

        print("All required directories have been checked and created if necessary.")
    
    def write_to_eclair_conf(self):
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

        conf_file_path = os.path.join(self.directory, 'eclair.config.json')

        with open(conf_file_path, 'w') as conf_file:
            json.dump(conf_data, conf_file, indent=4)

        print(f"eclair.config.json created with the following data:")
        print(conf_data)
    
    def initialize_project(self):
        self.get_user_input()
        self.check_and_create_directories()
        self.write_to_eclair_conf()

def flow():
    # Instantiate ProjectInitializer and initialize the project
    project = ProjectInitializer()
    project.initialize_project()
