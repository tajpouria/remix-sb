from brownie import network, accounts, config


LOCAL_CHAIN_ENVS = ["development"]


def get_owner_account():
    activate_net = network.show_active()

    if activate_net in LOCAL_CHAIN_ENVS:
        return accounts[-1]

    return accounts.add(config["wallets"][activate_net]["owner_private_key"])
