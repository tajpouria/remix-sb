from brownie import Lottery
from scripts.utils import get_key_hash, get_owner_accout, get_contract, get_verify


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


def main():
    deploy_lottery()
