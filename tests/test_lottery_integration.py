# 0.013
from scripts.deploy_lottery import deploy_lottery, get_account, fund_with_link, get_contract
from web3 import Web3
from scripts.helpfull_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS

from brownie import Lottery, accounts, config, network, exceptions
import time

def test_can_pick_winner():
    if network.show_active()  in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from":account, "value": lottery.getEntranceFee() + 1000})
    lottery.enter({"from":account, "value": lottery.getEntranceFee() + 1000})
    fund_with_link(lottery)
    lottery.endLottery({"from":account})
    time.sleep(60)
    assert lottery.recentWinner() == account
    assert lottery.balance == 0