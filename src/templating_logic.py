from jinja2 import Template
import ABI_class
from typing import Dict
import logging

def pure_view_no_input_no_output(abi_function: ABI_class.ContractABI.FunctionABI):
    name = abi_function.name
    template = f"""
def call_function_{name}(self) -> None:
    return self.call_function('{name}')
"""
    return template

def pure_view_no_input_output(abi_function: ABI_class.ContractABI.FunctionABI):
    name = abi_function.name
    outputs = abi_function.outputs  
    return_type = ", ".join(output.type for output in outputs)
    template = f"""
def call_function_{name}(self) -> ({return_type}):
    return self.call_function('{name}')
"""
    return template

def pure_view_input_no_output(abi_function: ABI_class.ContractABI.FunctionABI):
    name = abi_function.name
    inputs = abi_function.inputs
    input_type = ", ".join(input.type for input in inputs)
    template = f"""
def call_function_{name}(self, {input_type}) -> None:
    return self.call_function('{name}', {input_type})
"""
    return template

def pure_view_input_output(abi_function: ABI_class.ContractABI.FunctionABI):
    name = abi_function.name
    inputs = abi_function.inputs
    input_type = ", ".join(input.type for input in inputs)
    outputs = abi_function.outputs
    return_type = ", ".join(output.type for output in outputs)
    template = f"""
def call_function_{name}(self, {input_type}) -> ({return_type}):
    return self.call_function('{name}', {input_type})
"""
    return template

def exec_no_input_no_output(abi_function: ABI_class.ContractABI.FunctionABI):
    name = abi_function.name
    template = f"""
def execute_transaction_{name}(self) -> None:
    return self.execute_transaction('{name}')
"""
    return template

def exec_no_input_output(abi_function: ABI_class.ContractABI.FunctionABI):
    name = abi_function.name
    outputs = abi_function.outputs
    return_type = ", ".join(output.type for output in outputs)
    template = f"""
def execute_transaction_{name}(self) -> ({return_type}):
    return self.execute_transaction('{name}')
"""
    return template

def exec_input_no_output(abi_function: ABI_class.ContractABI.FunctionABI):
    name = abi_function.name
    inputs = abi_function.inputs
    input_type = ", ".join(input.type for input in inputs)
    template = f"""
def execute_transaction_{name}(self, {input_type}) -> None:
    return self.execute_transaction('{name}', {input_type})
"""
    return template

def exec_input_output(abi_function: ABI_class.ContractABI.FunctionABI):
    name = abi_function.name
    inputs = abi_function.inputs
    input_type = ", ".join(input.type for input in inputs)
    outputs = abi_function.outputs
    return_type = ", ".join(output.type for output in outputs)
    template = f"""
def execute_transaction_{name}(self, {input_type}) -> ({return_type}):
    return self.execute_transaction('{name}', {input_type})
"""
    return template

def create_function(abi_function: ABI_class.ContractABI.FunctionABI):
    logging.info(f"Creating function {abi_function.name}")
    name = abi_function.name
    inputs = abi_function.inputs
    outputs = abi_function.outputs
    state_mutability = abi_function.state_mutability
    if state_mutability != 'view' and state_mutability != 'pure':
        if not outputs and not inputs:
            template = "call function () -> ()"
            t = pure_view_no_input_no_output(abi_function)
        elif input and not outputs:
            template = "call function ({{inputs}}) -> ()"
            t = pure_view_input_no_output(abi_function)
        elif not inputs and outputs:
            template = "call function () -> ({{outputs}})"
            t = pure_view_no_input_output(abi_function)
        else:
            template = "call function ({{inputs}}) -> ({{outputs}})"
            t = pure_view_input_output(abi_function)
    else:
        if not outputs and not inputs:
            template = "exec function () -> ()"
            t = exec_no_input_no_output(abi_function)
        elif input and not outputs:
            template = "exec function ({{inputs}}) -> ()"
            t = exec_input_no_output(abi_function)
        elif not inputs and outputs:
            template = "exec function () -> ({{outputs}})"
            t = exec_no_input_output(abi_function)
        else:
            template = "exec function ({{inputs}}) -> ({{outputs}})"
            t = exec_input_output(abi_function)

    logging.info("%s: %s", abi_function.name, template)
    return t

abi = ABI_class.ContractABI(
    "/Users/abhinavmir/Desktop/Code/eclair/artifacts/contracts/payer.sol/PayeeContract.json")
for func in abi.functions:
    try:
        print(create_function(func))
    except Exception as e:
        print(e)
