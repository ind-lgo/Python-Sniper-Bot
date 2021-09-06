from web3 import Web3
import json

class Txn_bot():
    def __init__(self, token_address, quantity, slippage, gas_price, swap):
        self.w3 = self.connect()
        self.address, self.private_key = self.set_address()
        self.token_address = Web3.toChecksumAddress(token_address)
        self.token_contract = self.set_token_contract()
        self.utils_address, self.utils = self.set_Utils()
        self.router_address, self.router = self.set_router()
        self.quantity = quantity 
        self.slippage = 1 - (slippage/100)
        self.gas_price = gas_price
        self.SWAP = swap
        self.WBNB = Web3.toChecksumAddress("0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c")

    def connect(self):
        w3 = Web3(Web3.HTTPProvider("https://bsc-dataseed.binance.org/"))
        return w3

    def set_address(self):
        with open("./keys.json") as f:
            keys = json.load(f)
        if len(keys["metamask_address"]) <= 42:
            print("Set your Address in the key.json file!")
            exit()
        if len(keys.["metamask_private_key"]) <= 42:
            print("Set your PrivateKey in the key.json file!")
            exit()
        return(keys["metamask_address"], keys["metamask_private_key"])

    def get_token_decimals(self):
        return self.token_contract.functions.decimals().call()

    def set_Utils(self):
        Utils_address = Web3.toChecksumAddress("0x09029d284Eb0f9D28ec57a333062Ed1115e45771") 
        with open("./abis/DEX_Utils.json") as f:
            contract_abi = json.load(f)
        utils = self.w3.eth.contract(address=Utils_address, abi=contract_abi)
        return (Utils_address, utils)

    def set_router(self):
        router_address = Web3.toChecksumAddress("0x5F16809FF1705042da1AB84145D2C20d7D123803") 
        with open("./abis/TIGSRouterV1.json") as f:
            contract_abi = json.load(f)
        router = self.w3.eth.contract(address=router_address, abi=contract_abi)
        return (router_address, router)

    def set_token_contract(self):
        with open("./abis/bep20_abi_token.json") as f:
            contract_abi = json.load(f)
        token_contract = self.w3.eth.contract(address=self.token_address, abi=contract_abi)
        return token_contract

    def get_token_balance(self): 
        return self.token_contract.functions.balanceOf(self.address).call() / (10 ** self.token_contract.functions.decimals().call())

    def amountsOut_buy(self):
        Amount = self.utils.functions.getAmountsOut(
            int((self.quantity * (10** 18)) * self.slippage),
            [self.WBNB, self.token_address],
            self.SWAP
            ).call()
        return Amount


    def get_amounts_out_buy(self):
        Amount = self.utils.functions.getAmountsOut(
            int(self.quantity * self.slippage),
            [self.WBNB, self.token_address],
            self.SWAP
            ).call()
        return Amount


    def buy_token(self):
        self.quantity = self.quantity * (10 ** 18)
        txn = self.router.functions.makeBNBTokenSwap(
            int(self.get_amounts_out_buy()[1]),
            [self.WBNB, self.token_address],
            self.SWAP,
            self.address, 
        ).buildTransaction(
            {'from': self.address, 
            'gas': 780000,
            'gasPrice': self.gas_price,
            'nonce': self.w3.eth.getTransactionCount(self.address), 
            'value': int(self.quantity)}
            )
        signed_txn = self.w3.eth.account.sign_transaction(
            txn,
            self.private_key
        )
        txn = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        print("\nTX Hash:",txn.hex())
        txn_receipt = self.w3.eth.waitForTransactionReceipt(txn)
        if txn_receipt["status"] == 1: print("\nTransaction Successfull!")
        else: print("\nTransaction Faild!")



   
