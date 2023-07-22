# Eclair CLI Tool

## Description

Eclair is a Command Line Interface (CLI) tool designed to streamline the creation of library wrappers for Blockchain Business Logic code. With Eclair, you can initialize a new project and aggregate function definitions from solidity files, generating Python code as a result.

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
eclair
```

This will process Solidity files found in the `contracts` directory of your project, generate an ABI for each contract, and then generate a Python class for each ABI in the `wrappers` directory.

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