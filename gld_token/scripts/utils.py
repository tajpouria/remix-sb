from brownie import network, accounts, config


LOCAL_CHAIN_ENVS = ["development"]


def get_owner_accout():
    active_net = network.show_active()

    if active_net in LOCAL_CHAIN_ENVS:
        return accounts[0]

    return accounts.add(config["wallets"][active_net]["owner_private_key"])


def get_verify():
    return config["networks"][network.show_active()].get("verify", False)
