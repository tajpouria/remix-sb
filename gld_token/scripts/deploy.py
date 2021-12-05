from brownie import GLDToken
from scripts.utils import get_owner_accout, get_verify


INITIAL_SUPPLY = 10 * 10 ** 18


def deploy_gld_token(initial_supply=INITIAL_SUPPLY):
    return GLDToken.deploy(
        initial_supply, {"from": get_owner_accout()}, publish_source=get_verify()
    )


def main():
    deploy_gld_token()
