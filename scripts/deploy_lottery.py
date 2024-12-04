from brownie import accounts, config, Lottery, network
from scripts.helpfull_scripts import get_account, get_contract, fund_with_link
import time

def deploy_lottery():
   # print(accounts[0])
    account = get_account()
    #account = accounts.add(config["wallets"]["from_key"])
    lottery = Lottery.deploy (get_contract("eth_usd_price_feed").address, 
                              get_contract("vrf_coordinator").address, 
                              get_contract("link_token").address, 
                              config["networks"][network.show_active()]["fee"], 
                              config["networks"][network.show_active()]["keyhash"] 
                              ,{"from":account} )

    print("Deployed")
    return lottery

def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({"from":account})
    starting_tx.wait(1)
    print("loteria comenzada")

def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 1000000
    tx = lottery.enter({"from":account, "value": value })
    tx.wait(1)
    print("entrando a la loteria")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    # fund the contract
    tx = fund_with_link (lottery.address)
   # tx.wait(1)
    etx = lottery.endLottery({"from":account})
    etx.wait(1)
    time.sleep(60)
    print(f"{lottery.recentWinner()} Es el ganador")

def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
