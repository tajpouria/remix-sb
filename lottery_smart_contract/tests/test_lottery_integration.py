from py import log
import pytest
from time import sleep
from brownie import network
from scripts.utils import fund_with_link, get_local_chain_env, get_owner_accout
from scripts.deploy import deploy_lottery


def test_pick_lottery_winner_correctly():
    if network.show_active() in get_local_chain_env():
        pytest.skip()

    lottery = deploy_lottery()
    owner_acc = get_owner_accout()

    lottery.openLottery({"from": owner_acc}).wait(1)

    lottery.enterLottery({"from": owner_acc, "value": lottery.getEntranceFee()}).wait(1)

    fund_with_link(lottery.address)
    lottery.closeLottery({"from": owner_acc}).wait(1)

    sleep(60)
    assert lottery.recentWinner() == owner_acc
    assert lottery.balance() == 0
