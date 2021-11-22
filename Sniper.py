from txns import TXN
import argparse, math, sys, json, requests
from time import sleep
from halo import Halo
from style import style

ascii = """
  ______               ___                _______                     
 /_  __/________ _____/ (_)___  ____ _   /_  __(_)___ ____  __________
  / / / ___/ __ `/ __  / / __ \/ __ `/    / / / / __ `/ _ \/ ___/ ___/
 / / / /  / /_/ / /_/ / / / / / /_/ /    / / / / /_/ /  __/ /  (__  ) 
/_/ /_/   \__,_/\__,_/_/_/ /_/\__, /    /_/ /_/\__, /\___/_/  /____/  
                             /____/           /____/                  
"""
spinneroptions = {'interval': 250,'frames': ['🚀 ', '🌙 ', '🚀 ', '🌕 ', '💸 ']}
parser = argparse.ArgumentParser(description='Set your Token and Amount example: "sniper.py -t 0x34faa80fec0233e045ed4737cc152a71e490e2e3 -a 0.2 -s 15"')
parser.add_argument('-t', '--token', help='str, Token for snipe e.g. "-t 0x34faa80fec0233e045ed4737cc152a71e490e2e3"')
parser.add_argument('-a', '--amount',default=0, help='float, Amount in Bnb to snipe e.g. "-a 0.1"')
parser.add_argument('-tx', '--txamount', default=1, nargs="?", const=1, type=int, help='int, how mutch tx you want to send? It Split your BNB Amount in e.g. "-tx 5"')
parser.add_argument('-hp', '--honeypot', action="store_true", help='Check if your token to buy is a Honeypot, e.g. "-hp" or "--honeypot"')
parser.add_argument('-tp', '--takeprofit', default=0, nargs="?", const=True, type=int, help='int, Percentage TakeProfit from your input BNB amount "-tp 50" ')
parser.add_argument('-sl', '--stoplose', default=0, nargs="?", const=True, type=int, help='int, Percentage Stop lose from your input BNB amount "-sl 50" ')
parser.add_argument('-wb', '--awaitBlocks', default=0, nargs="?", const=True, type=int, help='int, Await Blocks before sending BUY Transaction "-ab 50" ')
parser.add_argument('-so', '--sellonly',  action="store_true", help='Sell all your Tokens from given address')
parser.add_argument('-bo', '--buyonly',  action="store_true", help='Buy Tokens with from your given amount')
args = parser.parse_args()


class SniperBot():
    def __init__(self):
        self.parseArgs()
        self.settings = self.loadSettings()
        self.SayWelcome()
    
    def loadSettings(self):
        with open("Settings.json","r") as settings:
            settings = json.load(settings)
        return settings

    def SayWelcome(self):
        print(style().YELLOW + ascii+ style().RESET)
        print(style().GREEN +"""Attention, You pay a 0.7% Tax on your swap amount!"""+ style().RESET)
        print(style().GREEN +"Start Sniper Tool with following arguments:"+ style().RESET)
        print(style().BLUE + "---------------------------------"+ style().RESET)
        print(style().YELLOW + "Amount for Buy:",style().GREEN + str(self.amount) + " BNB"+ style().RESET)
        print(style().YELLOW + "Token to Interact :",style().GREEN + str(self.token) + style().RESET)
        print(style().YELLOW + "Transaction to send:",style().GREEN + str(self.tx)+ style().RESET)
        print(style().YELLOW + "Amount per transaction :",style().GREEN + str("{0:.8f}".format(self.amountForSnipe))+ style().RESET)
        print(style().YELLOW + "Await Blocks before buy :",style().GREEN + str(self.wb)+ style().RESET)
        if self.tp != 0:
            print(style().YELLOW + "Take Profit Percent :",style().GREEN + str(self.tp)+ style().RESET)
            print(style().YELLOW + "Target Output for Take Profit:",style().GREEN +str("{0:.8f}".format(self.takeProfitOutput))+ style().RESET)
        if self.sl != 0:
            print(style().YELLOW + "Stop Lose Percent :",style().GREEN + str(self.sl)+ style().RESET)
            print(style().YELLOW + "Sell if Output is smaller as:",style().GREEN +str("{0:.8f}".format(self.stoplose))+ style().RESET)
        print(style().BLUE + "---------------------------------"+ style().RESET)
        
    def parseArgs(self):
        self.token = args.token
        if self.token == None:
            print(style.RED+"Please Check your Token argument e.g. -t 0x34faa80fec0233e045ed4737cc152a71e490e2e3")
            print("exit!")
            sys.exit()
        self.amount = args.amount  
        if not args.sellonly: 
            if self.amount == 0:
                print(style.RED+"Please Check your Amount argument e.g. -a 0.01")
                print("exit!")
                sys.exit()
        self.tx = args.txamount
        self.amountForSnipe = float(self.amount) / float(self.tx)
        self.hp = args.honeypot
        self.wb = args.awaitBlocks
        self.tp = args.takeprofit
        self.sl = args.stoplose 
        self.stoplose = 0
        self.takeProfitOutput = 0
        if self.tp != 0:
            self.takeProfitOutput = self.calcProfit()
        if self.sl != 0:
            self.stoplose = self.calcLose()

    def calcProfit(self):
        a = ((self.amountForSnipe * self.tx) * self.tp) / 100
        b = a + (self.amountForSnipe * self.tx)
        return b 
    
    def calcLose(self):
        a = ((self.amountForSnipe * self.tx) * self.sl) / 100
        b = (self.amountForSnipe * self.tx) - a
        return b 

    def getTaxHoneypot(self):
        url = f"https://ishoneypot.trading-tigers.com/token/{self.token}"
        r = requests.get(url)
        jres = json.loads(r.text)
        if jres['HONEYPOT']  == False:
            return False, jres['SELLTAX'], jres['BUYTAX']
        elif jres['HONEYPOT'] == True:
            return True, 0, 0

    def awaitBuy(self):
        spinner = Halo(text='await Buy', spinner=spinneroptions)
        spinner.start()
        for i in range(self.tx):
            spinner.start()
            self.TXN = TXN(self.token, self.amountForSnipe)
            tx = self.TXN.buy_token()
            spinner.stop()
            print(tx[1])
            if tx[0] != True:
                sys.exit() 

    def awaitSell(self):
        spinner = Halo(text='await Sell', spinner=spinneroptions)
        spinner.start()
        self.TXN = TXN(self.token, self.amountForSnipe)
        tx = self.TXN.sell_tokens()
        spinner.start()
        print(tx[1])
        if tx[0] != True:
            sys.exit() 

    def awaitApprove(self):
        spinner = Halo(text='await Approve', spinner=spinneroptions)
        spinner.start()
        self.TXN = TXN(self.token, self.amountForSnipe)
        tx = self.TXN.approve()
        spinner.stop()
        print(tx[1])
        if tx[0] != True:
            sys.exit() 

    def awaitBlocks(self):
        spinner = Halo(text='await Blocks', spinner=spinneroptions)
        spinner.start()
        waitForBlock = self.TXN.getBlockHigh() + self.wb
        while True:
            sleep(0.13)
            if self.TXN.getBlockHigh() > waitForBlock:
                spinner.stop()
                break
        print(style().GREEN+"[DONE] Wait Blocks finish!")
        
    def awaitLiquidity(self):
        spinner = Halo(text='await Liquidity', spinner=spinneroptions)
        spinner.start()
        while True:
            sleep(0.07)
            try:
                self.TXN.getOutputfromBNBtoToken()
                spinner.stop()
                break
            except Exception as e:
                print(e)
                if "UPDATE" in str(e):
                    print(e)
                    sys.exit()
                continue
        print(style().GREEN+"[DONE] Liquidity is Added!"+ style().RESET)
    
    def awaitProfitLose(self):
        TokenBalance = round(self.TXN.get_token_balance(),5)
        while True:
            sleep(0.3)
            Output = float(self.TXN.getOutputfromTokentoBNB() / (10**18))
            print(f"Token Balance: {TokenBalance} current output:", "{0:.8f}".format(Output), end="\r")

            if self.takeProfitOutput != 0:
                if Output >= self.takeProfitOutput:
                    print()
                    print(style().GREEN+"[TAKE PROFIT] Triggert!"+ style().RESET)
                    self.awaitSell()
                    break

            if self.stoplose != 0:
                if Output <= self.stoplose:
                    print()
                    print(style().GREEN+"[STOP LOSE] Triggert!"+ style().RESET)
                    self.awaitSell()
                    break
        print(style().GREEN+"[DONE] TakeProfit/StopLose Finished!"+ style().RESET)

    def StartUP(self):
        self.TXN = TXN(self.token, self.amountForSnipe)
        if args.sellonly:
            print("Start SellOnly, Selling Now all tokens!")
            inp = input("please confirm y/n\n")
            if inp.lower() == "y": 
                print(self.TXN.sell_tokens()[1])
                sys.exit()
            else:
                sys.exit()
        if args.buyonly:
            print(f"Start BuyOnly, buy now with {self.amountForSnipe}BNB tokens!")
            print(self.TXN.buy_token()[1])
            sys.exit()
        self.awaitLiquidity()
        honeyTax = self.getTaxHoneypot()
        if honeyTax[1] > self.settings["MaxSellTax"]:
            print(style().RED+"Token SellTax exceeds Settings.json, exiting!")
            sys.exit()
        if honeyTax[2] > self.settings["MaxBuyTax"]:
            print(style().RED+"Token BuyTax exceeds Settings.json, exiting!")
            sys.exit()
        if self.hp == True:
            print(style().YELLOW +"Checking Token is Honeypot..." + style().RESET)
            if honeyTax[0] == True:
                print(style.RED + "Token is Honeypot, exiting")
                sys.exit() 
            elif honeyTax[0] == False:
                print(style().GREEN +"[DONE] Token is NOT a Honeypot!" + style().RESET)
        if self.wb != 0: 
            self.awaitBlocks()
        self.awaitBuy()
        self.awaitApprove()
        if self.stoplose != 0 or self.takeProfitOutput != 0:
            self.awaitProfitLose()
        print(style().GREEN + "[DONE] TradingTigers Sniper Bot finish!" + style().RESET)


SniperBot().StartUP()
