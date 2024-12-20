from brownie import network, config, accounts, MockV3Aggregator, Contract, VRFCoordinatorMock, LinkToken

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

def get_account(index=None,id=None):
    # accounts
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    
    return accounts.add(config["wallets"]["from_key"])

contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator, "vrf_coordinator": VRFCoordinatorMock, "link_token": LinkToken
}

def get_contract(contract_name):
    """ Esta es una funcion de prueba

        Args:
            contract_name ( string )

        Returns:
            The most recently deployed version of this contract 
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            #MockV3Aggregator.length
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        # address
        # ABI
        contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi)
    return contract

DECIMALS=8
INITIAL_VALUE=200000000000

def deploy_mocks(decimals=DECIMALS, initial_value = INITIAL_VALUE):
    account=get_account()
    mock_price_feed = MockV3Aggregator.deploy(decimals, initial_value, {"from":account})
    link_token = LinkToken.deploy({"from":account})
    VRFCoordinatorMock.deploy(link_token.address,{"from":account})
    print( "desplegado")


def fund_with_link(contract_address, account=None, link_token=None, ammount=100000000000000000):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, ammount, {"from": account})
    tx.wait(1)
    print("contrato con fondos")
    return tx