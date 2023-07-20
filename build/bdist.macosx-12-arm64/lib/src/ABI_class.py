import json

class ContractABI:
    def __init__(self, file_path):
        self.file_path = file_path
        self.abi = self.read_abi_from_file(file_path)
        self.name = self.abi['contractName']
        self.functions = []
        self.constructor = None
        self.fallback = None
        self.receive = None

        for func in self.abi['abi']:
            if func['type'] == 'function':
                self.functions.append(self.FunctionABI(
                    name=func['name'],
                    inputs=func['inputs'],
                    outputs=func['outputs'],
                    state_mutability=func['stateMutability']
                ))
            elif func['type'] == 'constructor':
                self.constructor = self.NonFunctionABI(
                    inputs=func['inputs'],
                    name='Constructor',
                    outputs=[],
                    state_mutability=func['stateMutability'],
                    type=func['type']
                )
            elif func['type'] == 'fallback':
                self.fallback = self.NonFunctionABI(
                    inputs=[],
                    name='Fallback',
                    outputs=[],
                    state_mutability=func['stateMutability'],
                    type=func['type']
                )
            elif func['type'] == 'receive':
                self.receive = self.NonFunctionABI(
                    inputs=[],
                    name='Receive',
                    outputs=[],
                    state_mutability=func['stateMutability'],
                    type=func['type']
                )

    class FunctionABI:
        def __init__(self, name, inputs, outputs, state_mutability):
            self.name = name
            self.inputs = [ContractABI.Input(i['name'], i['type'], i['internalType']) for i in inputs]
            self.outputs = [ContractABI.Output(o['type'], o['internalType']) for o in outputs]
            self.state_mutability = state_mutability

        def __repr__(self):
            return f"└── FunctionABI(name={self.name}, inputs={self.inputs}, outputs={self.outputs}, state_mutability={self.state_mutability})"
        
    class Input:
        def __init__(self, name, type, internal_type):
            self.name = name
            self.internal_type = internal_type
            self.type = type
            self.pythonic_type = get_pythonic_type(type)

        def __repr__(self):
            return f"Input(name={self.name}, type={self.type}, pythonic_type={self.pythonic_type})"
    
    class Output:
        def __init__(self, type, internal_type):
            
            self.internal_type = internal_type
            self.type = type
            self.pythonic_type = get_pythonic_type(type)

        def __repr__(self):
            return f"type={self.type}, pythonic_type={self.pythonic_type})"

    class NonFunctionABI:
        def __init__(self, inputs, name, outputs, state_mutability, type):
            self.name = name
            self.inputs = [ContractABI.Input(i['name'], i['type'], i['internalType']) for i in inputs]
            self.outputs = [ContractABI.Output(o['type'], o['internalType']) for o in outputs]
            self.state_mutability = state_mutability
            self.type = type

        def __repr__(self):
            return f"└── NonFunctionABI(inputs={self.inputs}, name={self.name}, outputs={self.outputs}, state_mutability={self.state_mutability}, type={self.type})"

    def read_abi_from_file(self, file_path):
        with open(file_path, 'r') as file:
            abi_data = json.load(file)

        return abi_data

    def __repr__(self):
        repr_str = f"{self.name} @ {self.file_path})\n"
        repr_str += "├── functions:\n"
        for func in self.functions:
            repr_str += f"│   {repr(func)}\n"
        repr_str += f"├── constructor: {repr(self.constructor)}\n"
        repr_str += f"├── fallback: {repr(self.fallback)}\n"
        repr_str += f"└── receive: {repr(self.receive)}\n"
        return repr_str
    
def get_pythonic_type(type):
    if type == 'bool':
        return 'bool'
    elif type.startswith('uint') or type.startswith('int'):
        return 'int'
    elif type == 'address':
        return 'str'
    elif type.startswith('bytes'):
        return 'bytes'
    elif type == 'string':
        return 'str'
    elif type.startswith('mapping'):
        return 'dict'
    elif type.endswith('[]'):
        return 'list'
    else:
        return None  # if type not recognized
