import sys
import random
from threading import Timer

from web3 import Web3, HTTPProvider
from solc import compile_source, compile_files
from web3.contract import ConciseContract

from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

web3 = Web3(HTTPProvider('http://localhost:8545'))
history = InMemoryHistory()

class RepeatedTimer(object):
    def __init__(self, interval, contract, *args, **kwargs):
        self._timer     = None
        self.contract   = contract
        self.interval   = interval
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()
    def _run(self):
        self.is_running = False
        self.start()
        drop(self.contract)
    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True
    def stop(self):
        self._timer.cancel()
        self.is_running = False

class StakingSimulator():
    def __init__(self):
        self.stakeSimulator_interface = None
        self.stakeSimulator_contract = None
        self.stakeSimulator_address = None
        self.recipientCounter = None
        self.userInput = None
    
    def compile_contract(self, contract_file, contract_name):
        contract_sol = compile_source(contract_file)  # Compiled source code
        interface = contract_sol['<stdin>:' + contract_name]
        return interface
    
    def deploy_contract(self, interface, gas=4100000, arguments=None):
        # Instantiate and deploy contract
        contract = web3.eth.contract(abi=interface['abi'], bytecode=interface['bin'])
        
        # Get transaction hash from deployed contract
        tx_hash = contract.deploy(transaction={'from': web3.eth.accounts[0], 'gas': gas}, args=arguments)
        
        # Get tx receipt to get contract address
        tx_receipt = web3.eth.getTransactionReceipt(tx_hash)
        contract_address = tx_receipt['contractAddress']
        
        # Contract instance in concise mode
        contract_instance = web3.eth.contract(abi=interface['abi'], address=contract_address,
                                              ContractFactoryClass=ConciseContract)
        return contract_instance, contract_address
    
    def deployStakeSimulator(self,):
        with open('StakeSimulator.sol', 'r') as myfile:
            stakeSimulator_file = myfile.read()
        
        stakeSimulator_interface = self.compile_contract(stakeSimulator_file, 'StakeSimulator')
        (stakeSimulator_contract, stakeSimulator_address) = self.deploy_contract(stakeSimulator_interface, gas=6000000)
        print('Search Contract Address: ', stakeSimulator_address)
        return stakeSimulator_interface, stakeSimulator_contract, stakeSimulator_address
    
    def drop(self, contract):
        contract.drop(transact={'from': web3.eth.coinbase})
    
    def auto_configure(self, numUsers = 1, period = 15):
        recipientCounter = 0
        (stakeSimulator_interface, stakeSimulator_contract, stakeSimulator_address) = self.deployStakeSimulator()
        for i in range(numUsers):
            recipientCounter = recipientCounter + 1;
            stakeSimulator_contract.addRecipient(web3.eth.accounts[i], transact={'from': web3.eth.coinbase})
        stakeSimulator_contract.deposit(
                                        transact={'from': web3.eth.accounts[i], 'value': web3.toWei(str(random.randrange(85, 98)), 'ether')})
                                        dropTimer = RepeatedTimer(period, stakeSimulator_contract)
                                        return (stakeSimulator_interface, stakeSimulator_contract, stakeSimulator_address, dropTimer, recipientCounter)

def deploy(self):
    self.recipientCounter = 0
        (self.stakeSimulator_interface, self.stakeSimulator_contract, self.stakeSimulator_address) = self.deployStakeSimulator()
    
    def print(self):
        if self.stakeSimulator_address == '':
            print('No contract deployed.')
        else:
            print(self.stakeSimulator_address)

def add(self):
    address = self.userInput[37:]
    recipientCounter = self.recipientCounter + 1
        self.stakeSimulator_contract.addRecipient(address, transact={'from':web3.eth.coinbase})

    def remove(self):
        self.recipientCounter = self.recipientCounter - 1
        address = self.userInput[39:]
        self.stakeSimulator_contract.removeRecipient(address, transact={'from': web3.eth.coinbase})

def list(self):
    for i in range(self.recipientCounter):
        print(self.stakeSimulator_contract.recipients(i))

    def drop(self):
        self.drop(self.stakeSimulator_contract)

def period(self):
    period = self.userInput[38:]
    dropTimer = RepeatedTimer(period, self.drop(), args=(self.stakeSimulator_contract))
    
    def stop(self):
        self.dropTimer.stop()
    
    def start(self):
        self.dropTimer.start()
    
    def auto(self):
        (self.stakeSimulator_interface, self.stakeSimulator_contract, self.stakeSimulator_address, self.dropTimer,self.recipientCounter) = self.auto_configure(5)
    
    def run(self):
        command_completer = WordCompleter(['deploy','print', 'list','add','remove', 'stop', 'start', 'drop', 'period', 'auto'])
        commands_available = ['deploy','print', 'list','add','remove', 'stop', 'start', 'drop', 'period', 'auto']
        
        while 1:
            userInput = prompt('> ', completer=command_completer, history=history, auto_suggest=AutoSuggestFromHistory())
            self.userInput = userInput
            
            if userInput in commands_available:
                command = getattr(self, userInput)
                command()

def main():
    StakingSimulator stakingSim = StakingSimulator()
    stakingSim.start()


if __name__ == '__main__':
    main()
