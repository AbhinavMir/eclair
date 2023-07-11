import json

class ContractABI:
    def __init__(self, file_path):
        '''
        file_path: path to the json file containing the abi
        @NOTE doing this in a more effective way breaks the class creation for now, @TODO refactor ABI_class.py for better class creation
        '''
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
            self.inputs = inputs
            self.outputs = outputs
            self.state_mutability = state_mutability

        def __repr__(self):
            return f"└── FunctionABI(name={self.name}, inputs={self.inputs}, outputs={self.outputs}, state_mutability={self.state_mutability})"

    class NonFunctionABI:
        def __init__(self, inputs, name, outputs, state_mutability, type):
            self.inputs = inputs
            self.name = name
            self.outputs = outputs
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