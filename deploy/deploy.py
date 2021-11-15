from os import getenv
import json
from random import randrange
from pathlib import Path
from dotenv import load_dotenv
from solcx import compile_standard
from web3 import Web3

base_path = Path(__file__).parent.resolve()


load_dotenv(base_path / ".env")


with open(base_path / "contracts/SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"simpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
)

with open(base_path / "artifacts/combined.json", "w") as file:
    json.dump(compiled_sol, file)


w3 = Web3(Web3.HTTPProvider(getenv("PROVIDER_HTTP_ENDPOINT")))

abi = compiled_sol["contracts"]["simpleStorage.sol"]["SimpleStorage"]["abi"]

chain_id = int(getenv("PROVIDER_CHAIN_ID"))
owner_public_key = getenv("OWNER_PUBLIC_KEY")
owner_private_key = getenv("OWNER_PRIVATE_KEY")

owner_tx_count = w3.eth.getTransactionCount(owner_public_key)

print("Deplying the contract...")
tx_hash = w3.eth.send_raw_transaction(
    w3.eth.account.sign_transaction(
        w3.eth.contract(
            abi=abi,
            bytecode=compiled_sol["contracts"]["simpleStorage.sol"]["SimpleStorage"][
                "evm"
            ]["bytecode"]["object"],
        )
        .constructor()
        .buildTransaction(
            {"chainId": chain_id, "from": owner_public_key, "nonce": owner_tx_count}
        ),
        private_key=owner_private_key,
    ).rawTransaction
)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Contract deployed.")

simple_storage = w3.eth.contract(tx_receipt.contractAddress, abi=abi)

print(f"Initial store value: {simple_storage.functions.retrieve().call()}")

rand_value = randrange(1e18)

print(f"Sending store({rand_value}) transaction...")

tx_hash = w3.eth.send_raw_transaction(
    w3.eth.account.sign_transaction(
        simple_storage.functions.store(rand_value).buildTransaction(
            {
                "chainId": chain_id,
                "from": owner_public_key,
                "nonce": owner_tx_count + 1,
            }
        ),
        private_key=owner_private_key,
    ).rawTransaction
)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Store transaction completed.")

print(f"Final store value: {simple_storage.functions.retrieve().call()}")
