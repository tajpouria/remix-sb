from brownie import SimpleStorage


def get_value():
    simple_storage = SimpleStorage[-1]
    print(f"Value: {simple_storage.retrieve()}")


def main():
    get_value()
