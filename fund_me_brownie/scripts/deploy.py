from brownie import FundMe
from scripts.utils import get_owner_acc, get_price_feed_addr, get_verify_src


def deploy_fund_me():
    print(get_price_feed_addr())
    fund_me = FundMe.deploy(
        get_price_feed_addr(),
        {"from": get_owner_acc()},
        publish_source=get_verify_src(),
    )
    return fund_me


def main():
    deploy_fund_me()
