class Spoke:
    def __init__(self, private_key, deploy_args):
        # Update with your Ethereum node URL
        # (lz_address, lzc_value, compile) = deploy_args
        lz_address = deploy_args['lz_address']
        lzc_value = deploy_args['lzc_value']
        compile = deploy_args['compile']
        self.contract_address = deployer(lz_address, lzc_value, compile)[0]
        self.abi = deployer(lz_address, lzc_value, compile)[1]
        self.w3 = Web3(Web3.HTTPProvider("http://localhost:7545"))
        self.contract = self.w3.eth.contract(address=self.contract_address, abi=self.abi)
        self.w3.eth.default_account = self.w3.eth.account.from_key(
            '0x' + private_key).address
        self.private_key = private_key

    def call_function(self, function_name: str, *args) -> Dict:
        function = getattr(self.contract.functions, function_name)(*args)
        return function.call(
            {
                'from': self.w3.eth.default_account,
                'gas': 2000000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': self.w3.eth.get_transaction_count(self.w3.eth.default_account),
            }
        )

    def execute_transaction(self, function_name: str, *args) -> Dict:
        base_fee = self.w3.eth.gas_price * 40000
        function = getattr(self.contract.functions, function_name)(*args)
        transaction = function.build_transaction({
            'from': self.w3.eth.default_account,
            'gas': 2000000,
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

    def set_spoke(self, spoke_address: str, lzc: int) -> Dict:
        return self.execute_transaction('setSpoke', spoke_address, lzc)
    
    def place_taker(self, sell_token: str, buy_token: str, lz_cid: int, quantity: int) -> Dict:
        return self.execute_transaction('placeTaker', sell_token, buy_token, lz_cid, quantity)

    def place_maker(self, sell_token: str, buy_token: str, lz_cid: int, quantity: int, balance: int) -> Dict:
        return self.execute_transaction('placeMaker', sell_token, buy_token, lz_cid, quantity, balance)

    def delete_maker(self, sell_token: str, buy_token: str, lz_cid: int, maker_index: int) -> Dict:
        return self.execute_transaction('deleteMaker', sell_token, buy_token, lz_cid, maker_index)

    def get_takers(self, sell_token: str, buy_token: str, lz_cid: int) -> Dict:
        return self.call_function('getTakers', sell_token, buy_token, lz_cid)

    def get_makers(self, sell_token: str, buy_token: str, lz_cid: int) -> Dict:
        return self.call_function('getMakers', sell_token, buy_token, lz_cid)

    def get_contra_takers(self, sell_token: str, buy_token: str, lz_cid: int) -> Dict:
        return self.call_function('getContraTakers', sell_token, buy_token, lz_cid)

    def get_all_orders(self, sell_token: str, buy_token: str, lz_cid: int) -> Dict:
        return self.call_function('getAllOrders', sell_token, buy_token, lz_cid)

    def get_epoch(self, sell_token: str, buy_token: str, lz_cid: int) -> Dict:
        return self.call_function('getEpoch', sell_token, buy_token, lz_cid)

    def send(self, sell_token: str, buy_token: str, lz_cid: int) -> Dict:
        return self.execute_transaction('send', sell_token, buy_token, lz_cid)

    def accept(self, payload: Dict) -> Dict:
        return self.execute_transaction('accept', payload)

    def lz_receive(self, src_c: int, incoming_path: bytes, nonce: int, payload: bytes) -> Dict:
        return self.execute_transaction('lzReceive', src_c, incoming_path, nonce, payload)

    def set_config(self, version: int, chain_id: int, config_type: int, config: bytes) -> Dict:
        return self.execute_transaction('setConfig', version, chain_id, config_type, config)

    def force_resume_receive(self, src_chain_id: int, src_address: bytes) -> Dict:
        return self.execute_transaction('forceResumeReceive', src_chain_id, src_address)

    def set_receive_version(self, version: int) -> Dict:
        return self.execute_transaction('setReceiveVersion', version)

    def set_send_version(self, version: int) -> Dict:
        return self.execute_transaction('setSendVersion', version)

    def test(self) -> Dict:
        return self.call_function('testPrint')

    def transfer_event_listener(self) -> None:
        event_filter = self.contract.events.Transfer.createFilter(
            fromBlock="latest")
        for event in event_filter.get_all_entries():
            print("Token Sent:", event["args"]["token_sent"])
            print("Transfer From:", event["args"]["transfer_from"])
            print("Transfer To:", event["args"]["transfer_to"])
            print("Amount:", event["args"]["amount"])
            print("")