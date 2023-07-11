from web3 import Web3
import json

class TokenDeployer:
    def __init__(self, private_key, rpc_endpoint, erc20_file_path):
        self.private_key = private_key
        self.rpc_endpoint = rpc_endpoint
        self.erc20_file_path = erc20_file_path
        self.w3 = Web3(Web3.HTTPProvider(rpc_endpoint))
        self.account = self.w3.eth.account.from_key(private_key)

    def deploy_token(self):
        with open(self.erc20_file_path, 'r') as file:
            contract_dump = json.load(file)

        abi = contract_dump['abi']
        bytecode = contract_dump['bytecode']

        contract = self.w3.eth.contract(abi=abi, bytecode=bytecode)

        deploy_txn = contract.constructor().build_transaction({
            'from': self.account.address,
            'gas': 4443814,
            'gasPrice': self.w3.to_wei('0', 'gwei'),
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
        })

        signed_txn = self.account.sign_transaction(deploy_txn)
        deployment_receipt = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        contract_address = self.w3.eth.wait_for_transaction_receipt(deployment_receipt)['contractAddress']

        return contract_address

    def balance_of(self, token_address, address):
        with open(self.erc20_file_path, 'r') as file:
            contract_dump = json.load(file)

        abi = contract_dump['abi']
        contract = self.w3.eth.contract(address=token_address, abi=abi)

        balance = contract.functions.balanceOf(address).call()
        return balance

    def approved(self, token_address, address):
        with open(self.erc20_file_path, 'r') as file:
            contract_dump = json.load(file)

        abi = contract_dump['abi']
        contract = self.w3.eth.contract(address=token_address, abi=abi)

        approved = contract.functions.allowance(address, self.account.address).call()
        return approved

    def transfer(self, token_address, recipient_address, amount):
        with open(self.erc20_file_path, 'r') as file:
            contract_dump = json.load(file)

        abi = contract_dump['abi']
        contract = self.w3.eth.contract(address=token_address, abi=abi)

        transfer = contract.functions.transfer(recipient_address, amount).call()
        return transfer
