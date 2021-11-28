from brownie import network
from brownie import network
from brownie import network, accounts, exceptions
from web3 import Web3
import pytest
from scripts.deploy import deploy_fund_me
from scripts.utils import get_owner_acc, get_local_chain_envs


def test_can_fund_and_withdraw():
    fund_me = deploy_fund_me()
    acc = get_owner_acc()

    fund_amount = fund_me.getEntranceRate() + Web3.toWei(1, "ether")
    fund_me.fund({"from": acc, "value": fund_amount}).wait(1)
    assert fund_me.fundersDict(acc.address) == fund_amount

    fund_me.withdraw({"from": acc})
    assert fund_me.fundersDict(acc.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in get_local_chain_envs():
        pytest.skip("Only for run test on local chains")

    fund_me = deploy_fund_me()
    bad_acc = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_acc})
