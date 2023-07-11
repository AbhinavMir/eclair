import json
from ABI_class import ContractABI

def read_abi_from_file(filename):
    with open(filename, 'r') as file:
        abi_data = json.load(file)
    
    abi_entries = abi_data['abi']
    contract_abi = ContractABI()
    
    for entry in abi_entries:
        name = entry.get('name')
        inputs = entry.get('inputs', [])
        outputs = entry.get('outputs', [])
        state_mutability = entry.get('stateMutability')
        entry_type = entry.get('type')
        
        if entry_type == 'function':
            function_abi = FunctionABI(name, inputs, outputs, state_mutability)
            contract_abi.add_function(function_abi)
        elif entry_type == 'constructor':
            constructor_abi = ABIEntry(inputs, name, outputs, state_mutability, entry_type)
            contract_abi.constructor = constructor_abi
        elif entry_type == 'fallback':
            fallback_abi = ABIEntry([], name, [], state_mutability, entry_type)
            contract_abi.fallback = fallback_abi
        elif entry_type == 'receive':
            receive_abi = ABIEntry([], '', [], state_mutability, entry_type)
            contract_abi.receive = receive_abi
    
    return contract_abi

path = "/Users/abhinavmir/Desktop/Code/eclair/artifacts/contracts/payer.sol/PayeeContract.json"
contract_abi = read_abi_from_file(path)
print(contract_abi)