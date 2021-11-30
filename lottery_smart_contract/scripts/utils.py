from brownie import accounts, network, config


def get_fork_chain_envs():
    return ["mainnet-fork"]


def get_owner_accout():
    if network.show_active() in get_fork_chain_envs():
        return accounts[0]

    return accounts.add(config.wallets[network.show_active()].get("owner_account_addr"))


def get_price_feed_addr():
    return config["networks"][network.show_active()].get("price_feed_addr")
