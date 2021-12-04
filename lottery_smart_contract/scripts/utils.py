from brownie import (
    accounts,
    network,
    config,
    Contract,
    MockV3Aggregator,
    VRFCoordinatorMock,
    LinkToken,
)
from brownie.network import web3
from brownie.network.main import show_active


def get_key_hash():
    return config["networks"][network.show_active()]["key_hash"]


def get_verify():
    return config["networks"][network.show_active()].get("verify", False)


def get_fork_chain_envs():
    return ["mainnet-fork"]


def get_local_chain_env():
    return ["development"]


def get_owner_accout() -> network.account.LocalAccount:
    active_network = network.show_active()
    if (
        active_network in get_fork_chain_envs()
        or active_network in get_local_chain_env()
    ):
        return accounts[0]

    return accounts.add(config["wallets"][network.show_active()]["owner_private_key"])


def get_contract(
    contract_name: str,
    contract_to_mock={
        "MockV3Aggregator": MockV3Aggregator,
        "LinkToken": LinkToken,
        "VRFCoordinatorMock": VRFCoordinatorMock,
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
            config["networks"][show_active()][contract_name],
            contract_type.abi,
        )
    except KeyError:
        print(
            f"There is no contract address defined for contract {contract_name} in network {network.show_active()}"
        )


def deploy_contracts():
    MockV3Aggregator.deploy(8, 4530_00_000_000, {"from": get_owner_accout()})
    link_token = LinkToken.deploy({"from": get_owner_accout()})
    VRFCoordinatorMock.deploy(link_token.address, {"from": get_owner_accout()})


def fund_with_link(
    contract_addr, account=None, link_token=None, amount=web3.toWei(0.1, "ether")
):
    account = account if account else get_owner_accout()
    link_token = link_token if link_token else get_contract("LinkToken")
    tx = link_token.transfer(contract_addr, amount, {"from": account})
    tx.wait(1)
    return tx
