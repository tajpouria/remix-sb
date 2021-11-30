from brownie import Lottery
from scripts.utils import get_owner_accout, get_price_feed_addr


def deploy_lottery():
    lottery = Lottery.deploy(
        get_price_feed_addr(),
        {"from": get_owner_accout()},
    )

    return lottery


def main():
    deploy_lottery()
