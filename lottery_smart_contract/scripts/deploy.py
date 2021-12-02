from brownie import Lottery
from scripts.utils import get_owner_accout, get_price_feed_addr, get_contract


def deploy_lottery():
    mock_v3_aggregator = get_contract("MockV3Aggregator")

    lottery = Lottery.deploy(
        mock_v3_aggregator.address,
        {"from": get_owner_accout()},
    )

    return lottery


def main():
    deploy_lottery()
