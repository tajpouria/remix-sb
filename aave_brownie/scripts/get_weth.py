from brownie import interface, config
from brownie.network.main import show_active
from web3 import Web3

from scripts.utils import get_owner_account


def main():
    get_weth()


def get_weth():
    weth_token = interface.IWeth(config["networks"][show_active()]["weth_token"])
    weth_token.deposit(
        {"from": get_owner_account(), "value": Web3.toWei(0.1, "ether")}
    ).wait(1)
