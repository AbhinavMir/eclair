from jinja2 import Template
from .ABI_class import ContractABI
import logging

def initialise_class(rpc, private_key):
    template = f"""
    def __init__(self, rpc='{rpc}', private_key='{private_key}'):
        self.w3 = Web3(Web3.HTTPProvider('{rpc}'))
        self.deployed = Deployer(self.w3)
        self.contract_address = self.deployed['contract_address']
        self.abi = self.deployed['abi']
        self.contract = self.w3.eth.contract(address=self.contract_address, abi=self.abi)
        self.private_key = private_key
        """

    return template


def create_call_function():
    template = """
    def call_function(self, function_name: str, *args) -> Dict:
        function = getattr(self.contract.functions, function_name)(*args)
        return function.call(
            {
                'from': self.w3.eth.default_account,
                'gas': {},
                'gasPrice': self.w3.eth.gas_price,
                'nonce': self.w3.eth.get_transaction_count(self.w3.eth.default_account),
            }
        )
    """
    return template

def create_exec_function():
    template = """
    def execute_transaction(self, function_name: str, *args) -> Dict:
        base_fee = self.w3.eth.gas_price * {}
        function = getattr(self.contract.functions, function_name)(*args)
        transaction = function.build_transaction({
            'from': self.w3.eth.default_account,
            'gas': {},
            'gasPrice': self.w3.eth.gas_price,
            'nonce': self.w3.eth.get_transaction_count(self.w3.eth.default_account),
        })
        signed_transaction = self.w3.eth.account.sign_transaction(
            transaction, private_key=self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(
            signed_transaction.rawTransaction)
        self.w3.eth.wait_for_transaction_receipt(tx_hash)
        receipt = self.w3.eth.get_transaction_receipt(tx_hash)
        if receipt['status'] == 0:
            raise Exception('Transaction failed')
        elif receipt['status'] == 1:
            return {
                'txHash': tx_hash.hex(),
                'returns': receipt,
                'isSuccess': receipt['status'] == 1,
            }
        else:
            raise Exception('Unknown error')
    """
    return template


def pure_view_no_input_no_output(abi_function: ContractABI.FunctionABI):
    name = abi_function.name
    template = f"""
    def call_function_{name}(self) -> None:
        return self.call_function('{name}')
    """
    return template

def pure_view_no_input_output(abi_function: ContractABI.FunctionABI):
    name = abi_function.name
    outputs = abi_function.outputs  
    return_type = ", ".join(output.pythonic_type for output in outputs)

    if(len(outputs) > 1):
        return_type = f"Tuple({return_type})"

    template = f"""
    def call_function_{name}(self) -> ({return_type}):
        return self.call_function('{name}')
    """
    return template

def pure_view_input_no_output(abi_function: ContractABI.FunctionABI):
    name = abi_function.name
    inputs = abi_function.inputs
    input_params = ", ".join(f"{input.name}: {input.pythonic_type}" for input in inputs)
    input_param_without_type = ", ".join(input.name for input in inputs)
    template = f"""
    def call_function_{name}(self, {input_params}) -> None:
        return self.call_function('{name}', {input_param_without_type})
    """
    return template

def pure_view_input_output(abi_function: ContractABI.FunctionABI):
    name = abi_function.name
    inputs = abi_function.inputs
    input_params = ", ".join(f"{input.name}: {input.pythonic_type}" for input in inputs)
    input_param_without_type = ", ".join(input.name for input in inputs)
    outputs = abi_function.outputs
    return_type = ", ".join(output.pythonic_type for output in outputs)

    if(len(outputs) > 1):
        return_type = f"Tuple({return_type})"

    template = f"""
    def call_function_{name}(self, {input_params}) -> ({return_type}):
        return self.call_function('{name}', {input_param_without_type})
    """
    return template

def exec_no_input_no_output(abi_function: ContractABI.FunctionABI):
    name = abi_function.name
    template = f"""
    def execute_transaction_{name}(self) -> None:
        return self.execute_transaction('{name}')
    """
    return template

def exec_no_input_output(abi_function: ContractABI.FunctionABI):
    name = abi_function.name
    outputs = abi_function.outputs
    return_type = ", ".join(output.pythonic_type for output in outputs)

    if(len(outputs) > 1):
        return_type = f"Tuple({return_type})"

    template = f"""
    def execute_transaction_{name}(self) -> ({return_type}):
        return self.execute_transaction('{name}')
    """
    return template

def exec_input_no_output(abi_function: ContractABI.FunctionABI):
    name = abi_function.name
    inputs = abi_function.inputs
    input_params = ", ".join(f"{input.name}: {input.pythonic_type}" for input in inputs)
    input_param_without_type = ", ".join(input.name for input in inputs)
    template = f"""
    def execute_transaction_{name}(self, {input_params}) -> None:
        return self.execute_transaction('{name}', {input_param_without_type})
    """
    return template

def exec_input_output(abi_function: ContractABI.FunctionABI):
    name = abi_function.name
    inputs = abi_function.inputs
    input_params = ", ".join(f"{input.name}: {input.pythonic_type}" for input in inputs)
    input_param_without_type = ", ".join(input.name for input in inputs)
    outputs = abi_function.outputs
    return_type = ", ".join(output.pythonic_type for output in outputs)

    if(len(outputs) > 1):
        return_type = f"Tuple({return_type})"
        
    template = f"""
    def execute_transaction_{name}(self, {input_params}) -> ({return_type}):
        return self.execute_transaction('{name}', {input_param_without_type})
    """
    return template

def create_function(abi_function: ContractABI.FunctionABI):
    logging.info("Creating function %s", abi_function.name)
    name = abi_function.name
    inputs = abi_function.inputs
    outputs = abi_function.outputs
    state_mutability = abi_function.state_mutability

    # Check if the number of outputs is greater than 2
    if len(outputs) > 1:
        output_types = ", ".join(output.pythonic_type for output in outputs)
        return_type = f"Tuple({output_types})"
    else:
        return_type = ", ".join(output.pythonic_type for output in outputs)

    if state_mutability != 'view' and state_mutability != 'pure':
        if not outputs and not inputs:
            template = "call function () -> ()"
            t = pure_view_no_input_no_output(abi_function)
        elif input and not outputs:
            template = "call function ({{inputs}}) -> ()"
            t = pure_view_input_no_output(abi_function)
        elif not inputs and outputs:
            template = f"call function () -> ({return_type})"
            t = pure_view_no_input_output(abi_function)
        else:
            template = f"call function ({{inputs}}) -> ({return_type})"
            t = pure_view_input_output(abi_function)
    else:
        if not outputs and not inputs:
            template = "exec function () -> ()"
            t = exec_no_input_no_output(abi_function)
        elif input and not outputs:
            template = "exec function ({{inputs}}) -> ()"
            t = exec_input_no_output(abi_function)
        elif not inputs and outputs:
            template = f"exec function () -> ({return_type})"
            t = exec_no_input_output(abi_function)
        else:
            template = f"exec function ({{inputs}}) -> ({return_type})"
            t = exec_input_output(abi_function)

    logging.info("%s: %s", name, template)
    return t

def deployer_writer(
    run_compile: bool,
    constructor_args: list,
    network_name: str,
    private_key: str,
    abi_path: str,
    from_address: str,
    gas: int,
    gas_price: int,
    nonce: int
):
    template_code = """
def Deployer(w3):
    {% if run_compile %}
    os.system("npx hardhat compile")
    {% endif %}
    private_key = '{{ private_key }}'
    account = w3.eth.account.from_key(private_key)

    with open('{{ abi_path }}', 'r') as file:
        contract_dump = json.load(file)

    abi = contract_dump['abi']
    bytecode = contract_dump['bytecode']
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)

    deploy_txn = contract.constructor({{ constructor_args }}).buildTransaction({
        'from': '{{ from_address }}',
        'gas': {{ gas }},
        'gasPrice': {{ gas_price }},
        'nonce': {{ nonce }}
    })

    signed_txn = account.sign_transaction(deploy_txn)
    deployment_receipt = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    deployment_receipt = w3.eth.wait_for_transaction_receipt(deployment_receipt)
    contract_address = deployment_receipt['contractAddress']
    return {
        'contract_address': contract_address,
        'abi' : abi
    }
"""

    # Create a Jinja2 template object
    template = Template(template_code)

    # Render the template
    rendered_code = template.render(
        run_compile=run_compile,
        constructor_args=constructor_args,
        network_name=network_name,
        private_key=private_key,
        abi_path=abi_path,
        from_address=from_address,
        gas=gas,
        gas_price=gas_price,
        nonce=nonce
    )

    return rendered_code

def create_class(abi: ContractABI, args_from_config: dict):
    run_compile = args_from_config['run_compile']
    constructor_args = args_from_config['constructor_args']
    network_name = args_from_config['network_name']
    private_key = args_from_config['private_key']
    abi_path = args_from_config['abi_path']
    from_address = args_from_config['from_address']
    gas = args_from_config['gas']
    gas_price = args_from_config['gas_price']
    nonce = args_from_config['nonce']
    
    name = abi.name
    functions = abi.functions
    constructor = abi.constructor
    fallback = abi.fallback
    receive = abi.receive
    template = f"""
import os
import json
from typing import Dict, Tuple
from web3 import Web3
""" 
    template += deployer_writer(run_compile=run_compile,
        constructor_args=constructor_args,
        network_name=network_name,
        private_key=private_key,
        abi_path=abi_path,
        from_address=from_address,
        gas=gas,
        gas_price=gas_price,
        nonce=nonce
    )
    template += f"""
class contract_{name}_class:
"""
    template += initialise_class(network_name, private_key)
    template += create_call_function()
    template += create_exec_function()
    if constructor:
        template += create_function(constructor)
    if fallback:
        template += create_function(fallback)
    if receive:
        template += create_function(receive)
    
    for function in functions:
        template += create_function(function)
    return template