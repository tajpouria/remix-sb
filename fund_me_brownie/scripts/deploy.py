from brownie import FundMe, accounts, network, config


def deploy_fund_me():
    owner_acc = get_owner_acc()

    FundMe.deploy(get_price_feed_addr(), {"from": owner_acc}, publish_source=True)


def get_owner_acc():
    if network.show_active() == "development":
        return accounts[0]

    return accounts.add(config["wallets"]["owner_private_key"])


def get_price_feed_addr():
    return "0x8A753747A1Fa494EC906cE90E9f37563A8AF630e"


def main():
    deploy_fund_me()
