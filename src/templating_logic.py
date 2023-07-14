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
    return_type = ", ".join(output.pythonic_type for output in outputs)
    template = f"""
    def call_function_{name}(self) -> ({return_type}):
        return self.call_function('{name}')
    """
    return template

def pure_view_input_no_output(abi_function: ABI_class.ContractABI.FunctionABI):
    name = abi_function.name
    inputs = abi_function.inputs
    input_params = ", ".join(f"{input.name}: {input.pythonic_type}" for input in inputs)
    template = f"""
    def call_function_{name}(self, {input_params}) -> None:
        return self.call_function('{name}', {input_params})
    """
    return template

def pure_view_input_output(abi_function: ABI_class.ContractABI.FunctionABI):
    name = abi_function.name
    inputs = abi_function.inputs
    input_params = ", ".join(f"{input.name}: {input.pythonic_type}" for input in inputs)
    outputs = abi_function.outputs
    return_type = ", ".join(output.pythonic_type for output in outputs)
    template = f"""
    def call_function_{name}(self, {input_params}) -> ({return_type}):
        return self.call_function('{name}', {input_params})
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
    return_type = ", ".join(output.pythonic_type for output in outputs)
    template = f"""
    def execute_transaction_{name}(self) -> ({return_type}):
        return self.execute_transaction('{name}')
    """
    return template

def exec_input_no_output(abi_function: ABI_class.ContractABI.FunctionABI):
    name = abi_function.name
    inputs = abi_function.inputs
    input_params = ", ".join(f"{input.name}: {input.pythonic_type}" for input in inputs)
    template = f"""
    def execute_transaction_{name}(self, {input_params}) -> None:
        return self.execute_transaction('{name}', {input_params})
    """
    return template

def exec_input_output(abi_function: ABI_class.ContractABI.FunctionABI):
    name = abi_function.name
    inputs = abi_function.inputs
    input_params = ", ".join(f"{input.name}: {input.pythonic_type}" for input in inputs)
    outputs = abi_function.outputs
    return_type = ", ".join(output.pythonic_type for output in outputs)
    template = f"""
    def execute_transaction_{name}(self, {input_params}) -> ({return_type}):
        return self.execute_transaction('{name}', {input_params})
    """
    return template


def create_function(abi_function: ABI_class.ContractABI.FunctionABI):
    logging.info("Creating function %s", abi_function.name)
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

    logging.info("%s: %s", name, template)
    return t

def create_class(abi: ABI_class.ContractABI):
    name = abi.name
    functions = abi.functions
    constructor = abi.constructor
    fallback = abi.fallback
    receive = abi.receive
    template = f"""
class contract_{name}_class:
""" 
    if constructor:
        template += create_function(constructor)
    if fallback:
        template += create_function(fallback)
    if receive:
        template += create_function(receive)
    
    for function in functions:
        template += create_function(function)
    return template

abi = ABI_class.ContractABI(
    "/Users/abhinavmir/Desktop/Code/eclair/artifacts/contracts/payer.sol/PayeeContract.json")

print(create_class(abi))