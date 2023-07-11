from jinja2 import Template

template_code = """
import os, json; from web3 import Web3

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

    deploy_txn = contract.constructor().build_transaction({
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

contract_address = Deployer()

# Save rendered code to a file
output_filename = '{{ output_filename }}'
with open(output_filename, 'w') as output_file:
    output_file.write(rendered_code)
"""

# Create a Jinja2 template object
template = Template(template_code)

# Provide values for the template variables
run_compile = True  # Set to True to run "npx hardhat compile", False otherwise
network_name = 'http://example.com'  # Replace with the actual network name
private_key = 'your_private_key'  # Replace with your private key
abi_path = 'path_to_abi_file'  # Replace with the actual ABI file path
from_address = 'your_address'  # Replace with your address
gas = 200000  # Replace with the desired gas value
gas_price = 1000000000  # Replace with the desired gas price
nonce = 0  # Replace with the nonce value
output_filename = 'rendered_code.py'  # Replace with the desired output filename

# Render the template with the provided values
rendered_code = template.render(
    run_compile=run_compile,
    network_name=network_name,
    private_key=private_key,
    abi_path=abi_path,
    from_address=from_address,
    gas=gas,
    gas_price=gas_price,
    nonce=nonce,
    output_filename=output_filename
)

# Save the rendered code to a file
with open(output_filename, 'w') as output_file:
    output_file.write(rendered_code)
