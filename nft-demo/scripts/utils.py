from brownie import network, accounts, config


LOCAL_CHAINS = ["development"]

OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"


def get_owner_account():
    if network.show_active() in LOCAL_CHAINS:
        return accounts[0]

    return accounts.add(config["wallets"][network.show_active()]["owner_private_key"])
