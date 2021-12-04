import pytest
from brownie import network, exceptions
from web3 import Web3
from scripts.deploy import deploy_lottery
from scripts.utils import (
    USD_PRICE_FEED_INITIAL_ANSWER,
    fund_with_link,
    get_contract,
    get_local_accout,
    get_local_chain_env,
    get_owner_accout,
)


def test_get_entrance_fee():
    if network.show_active() not in get_local_chain_env():
        pytest.skip()

    lottery = deploy_lottery()
    entrance_fee = lottery.getEntranceFee()
    assert entrance_fee == Web3.toWei(
        (50 * 10 ** 7) / USD_PRICE_FEED_INITIAL_ANSWER, "ether"
    )


def test_cant_enter_unless_started():
    if network.show_active() not in get_local_chain_env():
        pytest.skip()

    lottery = deploy_lottery()
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enterLottery({"from": get_owner_accout()}).wait(1)


def test_can_start_and_enter_lottery():
    if network.show_active() not in get_local_chain_env():
        pytest.skip()

    lottery = deploy_lottery()
    owner_acc = get_owner_accout()

    lottery.openLottery({"from": owner_acc}).wait(1)
    lottery.enterLottery({"from": owner_acc, "value": lottery.getEntranceFee()}).wait(1)

    assert lottery.players(0) == owner_acc


def test_close_lottery():
    if network.show_active() not in get_local_chain_env():
        pytest.skip()

    lottery = deploy_lottery()
    owner_acc = get_owner_accout()

    lottery.openLottery({"from": owner_acc}).wait(1)
    lottery.enterLottery({"from": owner_acc, "value": lottery.getEntranceFee()}).wait(1)
    fund_with_link(lottery.address)
    lottery.closeLottery({"from": owner_acc}).wait(1)

    assert lottery.lotteryState() == 1


def test_pick_lottery_winner_correctly():
    if network.show_active() not in get_local_chain_env():
        pytest.skip()

    lottery = deploy_lottery()
    owner_acc = get_owner_accout()
    owner_acc_initial_balance = owner_acc.balance()

    lottery.openLottery({"from": owner_acc}).wait(1)
    lottery.enterLottery({"from": owner_acc, "value": lottery.getEntranceFee()}).wait(1)
    for i in range(1, 3):
        lottery.enterLottery(
            {"from": get_local_accout(i), "value": lottery.getEntranceFee()}
        ).wait(1)
    lottery_staked_balance = lottery.balance()

    fund_with_link(lottery.address)
    tx = lottery.closeLottery({"from": owner_acc})
    request_id = tx.events["RequestedRandomness"]["requestId"]
    tx.wait(1)

    STATIC_RNG = 777
    vrf_coordinator = get_contract("VRFCoordinatorMock")
    vrf_coordinator.callBackWithRandomness(
        request_id, STATIC_RNG, lottery.address, {"from": owner_acc}
    ).wait(1)

    assert lottery.recentWinner() == owner_acc
    assert lottery.balance() == 0
    print(owner_acc.balance())
    # assert owner_accout.balance() == owner_acc_initial_balance + lottery_staked_balance
