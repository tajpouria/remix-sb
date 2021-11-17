from brownie import SimpleStorage, accounts
from random import randrange


def test_deploy():
    owner_account = accounts[0]

    simple_storage = SimpleStorage.deploy({"from": owner_account})

    assert simple_storage.retrieve() == 0


def test_update_storage():
    owner_account = accounts[0]

    simple_storage = SimpleStorage.deploy({"from": owner_account})

    expected_val = randrange(1e18)

    simple_storage.store(expected_val, {"from": owner_account}).wait(1)

    assert simple_storage.retrieve() == expected_val
