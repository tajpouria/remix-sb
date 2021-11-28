from brownie import FundMe
from scripts.utils import get_owner_acc
from web3 import Web3


def fund():
    fund_me = FundMe[-1]

    entrance_rate = fund_me.getEntranceRate()
    fund_me.fund(
        {"from": get_owner_acc(), "value": entrance_rate + Web3.toWei(1, "ether")}
    )


def withdraw():
    fund_me = FundMe[-1]

    fund_me.withdraw({"from": get_owner_acc()})


def main():
    fund()
    withdraw()
