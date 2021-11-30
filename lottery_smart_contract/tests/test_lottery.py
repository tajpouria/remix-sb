from brownie import Lottery
from scripts.deploy import deploy_lottery


def test_get_entrance_fee():
    lottery = deploy_lottery()

    entrance_fee = lottery.getEntranceFee()
