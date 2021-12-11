from brownie import network
import pytest
from scripts.deploy_simple_collectible import (
    create_collectible,
    deploy_simple_collectible,
)
from scripts.utils import LOCAL_CHAINS, get_owner_account


def test_create_collectible():
    if network.show_active() not in LOCAL_CHAINS:
        pytest.skip()

    simple_collectible = deploy_simple_collectible()
    create_collectible(simple_collectible, "https://test.test")
    assert (
        simple_collectible.ownerOf(simple_collectible.latestTokenId())
        == get_owner_account()
    )
