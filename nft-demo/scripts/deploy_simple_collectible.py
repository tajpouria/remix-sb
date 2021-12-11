from brownie import config, network, SimpleCollectible

from scripts.utils import OPENSEA_URL, get_owner_account


def deploy_simple_collectible():
    return SimpleCollectible.deploy(
        {"from": get_owner_account()},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )


def create_collectible(simple_collectible, token_uri):
    simple_collectible.createCollectible(token_uri).wait(1)
    token_id = simple_collectible.latestTokenId()
    print(
        f"Visit on opensea: {OPENSEA_URL.format(simple_collectible.address, token_id)}"
    )


def main():
    simple_collectible = deploy_simple_collectible()
    create_collectible(
        simple_collectible,
        "https://ipfs.io/ipfs/QmZ1QMitqrm284tLi9ecJHMp9vLzMgzin2oeUDLnaqzXPR",
    )
