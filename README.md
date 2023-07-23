# Eclair CLI Tool

## Description

Eclair is a Command Line Interface (CLI) tool designed to streamline the creation of library wrappers for Blockchain Business Logic code. With Eclair, you can initialize a new project and run `eclair wrap` on it to generate Python library wrappers for your contracts. And since it dependes on the ABI, it can be used with any language that can generate an ABI.

## Installation

Eclair can be installed via pip:

```bash
pip install eclair
```

## Usage

### Initialize a Project

To initialize a new project, use the `init` command:

```bash
eclair init
```

During initialization, you will be asked to specify:

- The directory where you want to instantiate the project (default is the current directory).

- The preferred RPC endpoint (default is `localhost:7545`).

- The preferred Deployer address.

The tool will automatically create necessary directories and a configuration file in JSON format.

### Generate Python Library Wrappers

To generate Python library wrappers from your Solidity files, simply run Eclair with no arguments:

```bash
eclair wrap
```

This will process Solidity files found in the `contracts` directory of your project, generate an ABI for each contract, and then generate a Python class for each ABI in the `wrappers` directory.

### Example

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.6;

contract HelloWorld {
    string public greet = "Hello, World!";

    function sayHello() public view returns (string memory) {
        return greet;
    }
}
```
```python

import os
import json
from typing import Dict, Tuple
from web3 import Web3

def Deployer(w3):
    
    os.system("npx hardhat compile")
    
    private_key = 'your_private_key'
    account = w3.eth.account.from_key(private_key)

    with open('path_to_abi_file', 'r') as file:
        contract_dump = json.load(file)

    abi = contract_dump['abi']
    bytecode = contract_dump['bytecode']
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)

    deploy_txn = contract.constructor([]).buildTransaction({
        'from': 'your_address',
        'gas': 200000,
        'gasPrice': 1000000000,
        'nonce': 0
    })

    signed_txn = account.sign_transaction(deploy_txn)
    deployment_receipt = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    deployment_receipt = w3.eth.wait_for_transaction_receipt(deployment_receipt)
    contract_address = deployment_receipt['contractAddress']
    return {
        'contract_address': contract_address,
        'abi' : abi
    }
class contract_HelloWorld_class:

    def __init__(self, rpc='http://example.com', private_key='your_private_key'):
        self.w3 = Web3(Web3.HTTPProvider('http://example.com'))
        self.deployed = Deployer(self.w3)
        self.contract_address = self.deployed['contract_address']
        self.abi = self.deployed['abi']
        self.contract = self.w3.eth.contract(address=self.contract_address, abi=self.abi)
        self.private_key = private_key
        
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
    
    def execute_transaction_greet(self) -> (str):
        return self.execute_transaction('greet')
    
    def execute_transaction_sayHello(self) -> (str):
        return self.execute_transaction('sayHello')
```

## Configuration

Eclair's behavior can be customized via the `eclair.config.json` file in your project directory. This file is created when you initialize a project and includes a number of settings:

- `run_compile`: Whether to compile the Solidity files before processing (default is `true`).

- `constructor_args`: Arguments to be passed to the contract constructor when deploying.

- `network_name`: Network to deploy to (e.g., `http://example.com`).

- `private_key`: Your private key for signing transactions.

- `abi_path`: Path to the ABI file for the contract.

- `from_address`: Your address (will be used as the sender of transactions).

- `gas`: Gas limit for transactions.

- `gas_price`: Gas price for transactions.

- `nonce`: Nonce for transactions.

- `output_directory`: Directory to output the Python wrapper classes to (default is `wrappers`).

## Contributing

Contributions to Eclair are welcome! Please read our contributing guidelines for how to proceed.

## License

Eclair is released under the MIT License. See the LICENSE file for more details.

## Contact

If you have any issues or feature requests, please open an issue on the Eclair GitHub page. For other inquiries, you can reach out ioc.exchange/@formalcurryfication ~!

MIT License can be accessed [here](https://www.mit.edu/~amini/LICENSE.md)