from brownie import interface, config
from brownie.network.main import show_active
from web3 import Web3

from scripts.utils import get_owner_account


def main():
    # get_weth()
    lending_pool = get_lending_pool()
    get_user_account_data(lending_pool)


def get_weth():
    weth_token = interface.IWeth(config["networks"][show_active()]["weth_token"])
    weth_token.deposit(
        {"from": get_owner_account(), "value": Web3.toWei(0.1, "ether")}
    ).wait(1)


def get_user_account_data(lending_pool):
    (
        totalCollateralETH,
        totalDebtETH,
        availableBorrowsETH,
        currentLiquidationThreshold,
        ltv,
        healthFactor,
    ) = lending_pool.getUserAccountData(get_owner_account())

    return (
        float(totalCollateralETH),
        float(totalDebtETH),
        float(availableBorrowsETH),
        float(currentLiquidationThreshold),
        float(ltv),
        float(healthFactor),
    )


def get_lending_pool():
    lendingPoolAddressesProvider = interface.ILendingPoolAddressesProvider(
        config["networks"][show_active()]["lending_pool_addresses_provider"]
    )
    lending_pool_addr = lendingPoolAddressesProvider.getLendingPool()
    return interface.ILendingPool(lending_pool_addr)
