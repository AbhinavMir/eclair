
import os
import json
from web3 import Web3

def Deployer():
    
    os.system("npx hardhat compile")
    
    w3 = Web3(Web3.HTTPProvider('http://example.com'))
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
    return contract_address
