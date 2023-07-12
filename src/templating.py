from jinja2 import Template; import ABI_class as ABI_class

def create_python_file_from_abi_class(abi_class: ABI_class.ContractABI):
    pass

def create_execute_function(abi_function: ABI_class.ContractABI.FunctionABI):
    name = abi_function.name
    inputs = abi_function.inputs
    outputs = abi_function.outputs
    state_mutability = abi_function.state_mutability

    if state_mutability != 'view' and state_mutability != 'pure':
        template = f"""def execute_{name}(self, {", ".join([f"{arg.name}: {arg.type}" for arg in inputs])}) -> {outputs[0].type}:
    return self.call_function('{name}', {", ".join([arg.name for arg in inputs])})"""
    else:
        template = f"""def {name}(self, {", ".join([f"{arg.name}: {arg.type}" for arg in inputs])}) -> {outputs[0].type}:
    return self.call_function('{name}', {", ".join([arg.name for arg in inputs])})"""

    return template
