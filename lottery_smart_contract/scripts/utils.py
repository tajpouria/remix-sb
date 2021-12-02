from brownie import (
    accounts,
    network,
    config,
    Contract,
    MockV3Aggregator,
    VRFCoordinatorMock,
    LinkToken,
)
from brownie.network.main import show_active


def get_fork_chain_envs() -> list[str]:
    return ["mainnet-fork"]


def get_local_chain_env() -> list[str]:
    return ["development"]


def get_owner_accout() -> network.account.LocalAccount:
    if network.show_active() in get_fork_chain_envs():
        return accounts[0]

    return accounts.add(config.wallets[network.show_active()].get("owner_account_addr"))


def get_contract(
    contract_name: str,
    contract_to_mock={
        "MockV3Aggregator": MockV3Aggregator,
    },
):
    contract_type = contract_to_mock[contract_name]

    if network.show_active() in get_local_chain_env():
        if len(contract_type) == 0:
            deploy_contracts()
        return contract_type[-1]

    try:
        return Contract.from_abi(
            contract_type._name,
            config.networks[show_active()][contract_name],
            contract_type.abi,
        )
    except KeyError:
        print(
            f"There is no contract address defined for contract {contract_name} in network {network.show_active()}"
        )


def deploy_contracts():
    MockV3Aggregator.deploy(8, 4530_00_000_000)
    VRFCoordinatorMock.deploy()
