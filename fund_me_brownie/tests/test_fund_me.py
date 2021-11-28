from web3 import Web3
from scripts.deploy import deploy_fund_me
from scripts.utils import get_owner_acc


def test_can_fund_and_withdraw():
    fund_me = deploy_fund_me()
    acc = get_owner_acc()

    fund_amount = fund_me.getEntranceRate() + Web3.toWei(1, "ether")
    fund_me.fund({"from": acc, "value": fund_amount}).wait(1)
    assert fund_me.fundersDict(acc.address) == fund_amount

    fund_me.withdraw({"from": acc})
    assert fund_me.fundersDict(acc.address) == 0
