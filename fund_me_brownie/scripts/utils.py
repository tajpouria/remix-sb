from brownie import accounts, network, config, MockV3Aggregator


def get_local_chain_envs():
    return ["development", "ganache-local"]


def get_owner_acc():
    if network.show_active() in get_local_chain_envs():
        return accounts[0]

    return accounts.add(config["wallets"]["owner_private_key"])


def get_price_feed_addr():
    if network.show_active() in get_local_chain_envs():
        if len(MockV3Aggregator) < 1:
            deploy_mock_price_feed()

        return MockV3Aggregator[-1].address

    return config["networks"][network.show_active()].get("price_feed_addr")


def deploy_mock_price_feed():
    MockV3Aggregator.deploy(8, (4000 * 10 ** 8), {"from": get_owner_acc()})


def get_verify_src():
    return config["networks"][network.show_active()].get("verify_src")
