# 0.013
from scripts.deploy_lottery import deploy_lottery, get_account, fund_with_link
from web3 import Web3
from scripts.helpfull_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS

from brownie import Lottery, accounts, config, network, exceptions
import pytest

def test_get_entrance_fee():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    #arrange
    lottery = deploy_lottery()
    #act
    expected_entrance_fee = Web3.to_wei(50/2000, "ether")
    entrance_fee = lottery.getEntranceFee()
    #assert
    assert expected_entrance_fee == entrance_fee



def test_can_enter_unless_started():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
     #arrange
    lottery = deploy_lottery()
    
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from":get_account(), "value": lottery.getEntranceFee()})
   
  
def test_can_start_and_enter_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
     #arrange
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from":account})
    lottery.enter({"from":account, "value": lottery.getEntranceFee()})
    assert lottery.players(0) == account
   

def test_can_end_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
     #arrange
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from":account})
    lottery.enter({"from":account, "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    lottery.endLottery({"from":account})
    assert lottery.lottery_state() == 2

    
    def test_can_pick_winner_correctly():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
     #arrange
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from":account})
    lottery.enter({"from":account, "value": lottery.getEntranceFee()})
    lottery.enter({"from":get_account(index=1), "value": lottery.getEntranceFee()})
    lottery.enter({"from":get_account(index=2), "value": lottery.getEntranceFee()})

    fund_with_link(lottery)
    lottery.endLottery({"from":account})
   
    
    