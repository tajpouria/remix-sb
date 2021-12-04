from brownie import Lottery
from scripts.utils import (
    get_key_hash,
    get_owner_accout,
    get_contract,
    get_verify,
    fund_with_link,
)
from time import sleep


def deploy_lottery():
    lottery = Lottery.deploy(
        get_contract("MockV3Aggregator").address,
        get_contract("VRFCoordinatorMock").address,
        get_contract("LinkToken").address,
        get_key_hash(),
        {"from": get_owner_accout()},
        publish_source=get_verify(),
    )

    return lottery


def open_lottery(lottery):
    lottery.openLottery({"from": get_owner_accout()}).wait(1)


def enter_lottery(lottery):
    lottery.enterLottery({"from": get_owner_accout()}).wait(1)


def close_lottery(lottery):
    lottery.closeLottery({"from": get_owner_accout()}).wait(1)
    sleep(10)
    print(f"{lottery.recentWinner()} is the winner!")


def main():
    lottery = deploy_lottery()
    open_lottery(lottery)
    enter_lottery(lottery)
    fund_with_link(lottery.address)
    close_lottery(lottery)
