from random import randrange
from brownie import accounts, config, SimpleStorage, network


def deploy_simple_storage():
    owner_acc = get_owner_account()

    simple_storage = SimpleStorage.deploy({"from": owner_acc})

    print(f"Initial value: {simple_storage.retrieve()}")

    simple_storage.store(randrange(1e18)).wait(1)

    print(f"Final value: {simple_storage.retrieve()}")


def get_owner_account():
    if network.show_active() == "development":
        return accounts[0]

    return accounts.add(config["wallets"]["owner_private_key"])


def main():
    deploy_simple_storage()
