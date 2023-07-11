from jinja2 import Template
from src import ABI_class

def create_python_file_from_abi_class(abi_class: ABI_class.ContractABI):
    print(abi_class.name)