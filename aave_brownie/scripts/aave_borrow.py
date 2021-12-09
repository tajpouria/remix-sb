from brownie import interface, config, network
from brownie.network.main import show_active
from web3 import Web3

from scripts.utils import get_owner_account


def main():
    lending_pool = get_lending_pool()

    deposit_amount = Web3.toWei(0.1, "ether")
    approve_weth(lending_pool.address, deposit_amount)
    # deposit_weth(lending_pool, deposit_amount)
    _, availableBorrowsETH = get_user_account_data(lending_pool)
    dai_price = get_dai_price()
    dai_amount_to_borrow = (1 / dai_price) * (availableBorrowsETH * 0.95)
    print(dai_amount_to_borrow)
    # borrow_dai(lending_pool, dai_amount_to_borrow)
    approve_erc20(
        config["networks"][show_active()]["dai_token"],
        lending_pool.address,
        dai_amount_to_borrow,
    )
    repay_all(lending_pool, dai_amount_to_borrow)


def approve_erc20(token_addr, spender_addr, amount):
    dai_token = interface.IERC20(token_addr)
    dai_token.approve(spender_addr, amount, {"from": get_owner_account()}).wait(1)


def repay_all(lending_pool, amount):
    lending_pool.repay(
        config["networks"][show_active()]["dai_token"],
        amount,
        1,
        get_owner_account().address,
        {"from": get_owner_account()},
    ).wait(1)


def borrow_dai(lending_pool, amount):
    lending_pool.borrow(
        config["networks"][show_active()]["dai_token"],
        amount,
        1,
        0,
        get_owner_account().address,
        {"from": get_owner_account()},
    ).wait(1)


def deposit_weth(lending_pool, amount):
    lending_pool.deposit(
        config["networks"][network.show_active()]["weth_token"],
        amount,
        get_owner_account().address,
        0,
        {"from": get_owner_account()},
    ).wait(1)


def approve_weth(spender_addr, value):
    weth_token = interface.IWeth(config["networks"][show_active()]["weth_token"])
    tx = weth_token.approve(spender_addr, value, {"from": get_owner_account()})
    tx.wait(1)
    return tx


def get_user_account_data(lending_pool):
    _, totalDebtETH, availableBorrowsETH, _, _, _ = lending_pool.getUserAccountData(
        get_owner_account()
    )

    return float(totalDebtETH), float(availableBorrowsETH)


def get_lending_pool():
    lendingPoolAddressesProvider = interface.ILendingPoolAddressesProvider(
        config["networks"][show_active()]["lending_pool_addresses_provider"]
    )
    lending_pool_addr = lendingPoolAddressesProvider.getLendingPool()
    return interface.ILendingPool(lending_pool_addr)


def get_dai_price():
    dai_price_feed = interface.IAggregatorV3(
        config["networks"][show_active()]["dai_eth_price_feed"]
    )
    _, answer, _, _, _ = dai_price_feed.latestRoundData()

    return float(Web3.fromWei(answer, "ether"))
