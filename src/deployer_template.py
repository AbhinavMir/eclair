from jinja2 import Template
import os
import json
from web3 import Web3

def deployer_writer(
    run_compile: bool,
    constructor_args: list,
    network_name: str,
    private_key: str,
    abi_path: str,
    from_address: str,
    gas: int,
    gas_price: int,
    nonce: int,
    output_filename: str,
):
    template_code = """
import os
import json
from web3 import Web3

def Deployer():
    {% if run_compile %}
    os.system("npx hardhat compile")
    {% endif %}
    w3 = Web3(Web3.HTTPProvider('{{ network_name }}'))
    private_key = '{{ private_key }}'
    account = w3.eth.account.from_key(private_key)

    with open('{{ abi_path }}', 'r') as file:
        contract_dump = json.load(file)

    abi = contract_dump['abi']
    bytecode = contract_dump['bytecode']
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)

    deploy_txn = contract.constructor({{ constructor_args }}).buildTransaction({
        'from': '{{ from_address }}',
        'gas': {{ gas }},
        'gasPrice': {{ gas_price }},
        'nonce': {{ nonce }}
    })

    signed_txn = account.sign_transaction(deploy_txn)
    deployment_receipt = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    deployment_receipt = w3.eth.wait_for_transaction_receipt(deployment_receipt)
    contract_address = deployment_receipt['contractAddress']
    return contract_address

"""

    # Create a Jinja2 template object
    template = Template(template_code)

    # Render the template
    rendered_code = template.render(
        run_compile=run_compile,
        constructor_args=constructor_args,
        network_name=network_name,
        private_key=private_key,
        abi_path=abi_path,
        from_address=from_address,
        gas=gas,
        gas_price=gas_price,
        nonce=nonce,
        output_filename=output_filename
    )

    # Save rendered code to a file
    with open(output_filename, 'w') as output_file:
        output_file.write(rendered_code)

    return rendered_code

def write_rendered_code_to_file(rendered_code: str, output_filename: str):
    with open(output_filename, 'w') as output_file:
        output_file.write(rendered_code)

# Provide values for the template variables
run_compile = True  # Set to True to run "npx hardhat compile", False otherwise
constructor_args = []  # Replace with the constructor arguments
network_name = 'http://example.com'  # Replace with the actual network name
private_key = 'your_private_key'  # Replace with your private key
abi_path = 'path_to_abi_file'  # Replace with the actual ABI file path
from_address = 'your_address'  # Replace with your address
gas = 200000  # Replace with the desired gas value
gas_price = 1000000000  # Replace with the desired gas price
nonce = 0  # Replace with the nonce value
output_filename = 'rendered_code.py'  # Replace with the desired output filename

# Render the template
rendered_code = deployer_writer(
    run_compile=run_compile,
    constructor_args=constructor_args,
    network_name=network_name,
    private_key=private_key,
    abi_path=abi_path,
    from_address=from_address,
    gas=gas,
    gas_price=gas_price,
    nonce=nonce,
    output_filename=output_filename
)

print(rendered_code)
# Write the rendered code to a file
# write_rendered_code_to_file(rendered_code, output_filename)
