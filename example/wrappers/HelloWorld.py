
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
    