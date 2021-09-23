
from txns import Txn_bot
from time import sleep
import argparse, math
from honeypotChecker import HoneyPotChecker
from halo import Halo
from threading import Thread

parser = argparse.ArgumentParser(description='Set your Token and Amount example: "sniper.py -t 0x34faa80fec0233e045ed4737cc152a71e490e2e3 -a 0.2 -s 15"')
parser.add_argument('-t', '--token', help='str, Token for snipe e.g. "-t 0x34faa80fec0233e045ed4737cc152a71e490e2e3"')
parser.add_argument('-a', '--amount', help='float, Amount in Bnb to snipe e.g. "-a 0.1"')
parser.add_argument('-s', '--slippage', default=10, nargs="?", const=1, type=int, help='int, slippage in % "-s 10"')
parser.add_argument('-tx', '--txamount', default=1, nargs="?", const=1, type=int, help='int, how mutch tx you want to send? It Split your BNB Amount in e.g. "-tx 5"')
parser.add_argument('-hp', '--honeypot', default=True, nargs="?", const=True, type=bool, help='bool, check if your token to buy is a Honeypot, e.g. "-hp True"')
parser.add_argument('-swap', '--swap', default=[1], type=list, help='list, Witch Swap? e.g. "-swap [1] for Panackeswap"')
parser.add_argument('-tp', '--takeprofit', default=0, nargs="?", const=True, type=int, help='int, Percentage TakeProfit from your input BNB amount, if 0 then not used. e.g. "-tp 50" ')
parser.add_argument('-wb', '--awaitBlocks', default=0, nargs="?", const=True, type=int, help='int, Await Blocks bevore sending BUY Transaction, if 0 then not used. e.g. "-ab 50" ')
args = parser.parse_args()




TXN = int(args.txamount)
SNIPEquantity = (float(args.amount) / TXN)
slippage = int(args.slippage)
token=args.token
checkHoney = bool(args.honeypot)
swap = args.swap
takeprofit = int(args.takeprofit)
waitingBlocks = int(args.awaitBlocks)
gas_price = 6 * (10**9)

TIGS = Txn_bot(token_address="0x34faa80fec0233e045ed4737cc152a71e490e2e3", quantity=0, slippage=slippage, gas_price=gas_price, swap=swap)
TIGSBALANCE = TIGS.get_token_balance()

 
print("")
if TIGSBALANCE >= 100:
    Time = 0.1
    print("Welcome Premium Tiger!\nSet Checktime to " + str(Time) + " seconds")
else:
    Time = 5
    print("Welcome Tiger Buy 100 TIGS to get faster checktime.\nSet Checktime to " + str(Time) + " seconds")
Timer = float(Time)


def calcProfitExit():
    a = ((SNIPEquantity * TXN) * takeprofit) / 100
    b = a + (SNIPEquantity * TXN)
    return b 
    
profit = "not activated"
if takeprofit != 0: 
    profit = calcProfitExit() 
else:
    profit = 0
del TIGS, TIGSBALANCE


print("")
print("Start Sniper with following arguments")
print("---------------------------------------------------")
print("Amount for Buy:", str(args.amount) , "BNB")
print("Token to Snipe :", args.token)
print("Slippage :", str(args.slippage) + "%")
print("Transaction to send:", str(args.txamount))
print("Amount per transaction :", str(SNIPEquantity))
print("Await Blocks before buy :", str(waitingBlocks))
print("Take Profit Percent :", str(takeprofit))
print("Min Output from Take Profit:",str(profit))
print("---------------------------------------------------")


def checkIsHoneypot():
    isHoney = HoneyPotChecker(token).Is_Honeypot()
    return isHoney


def checkProfit():
    spinner = Halo(text='Checking Profit', spinner='dots')
    spinner.start()
    pbot = Txn_bot(
                    token_address=token,
                    quantity=SNIPEquantity,
                    slippage=slippage,
                    gas_price=gas_price,
                    swap=swap
                    )
    txn = pbot.approve()
    print(txn[1])
    sleep(3)
    tq = math.floor(pbot.get_token_balance()* 10000000)/10000000.0
    cbot = Txn_bot(
                    token_address=token,
                    quantity=tq,
                    slippage=slippage,
                    gas_price=gas_price,
                    swap=swap
                    )
    spinner.stop()
    sleep(3)
    while True:
        try:
            sleep(Timer)
            currentProfit = (cbot.amountsOut_sell()[1] /(10**18))
            print("Current Min Output from your Tokens", round(currentProfit,4), end="\r")
            if currentProfit >= profit:
                print("Profit reached, Sell now all Tokens.")
                sbot = Txn_bot(
                    token_address=token,
                    quantity=tq,
                    slippage=slippage,
                    gas_price=gas_price,
                    swap=swap)
                tx = sbot.sell_token()
                print(tx[1])
                if tx[0] == False:
                    exit()
                break
        except Exception as e:
            print(e)
            break

          
def waitBlocks():
    spinner = Halo(text='Waiting Blocks', spinner='dots')
    spinner.start()
    blocksbot = Txn_bot(token_address=token, quantity=0, slippage=0, gas_price=gas_price, swap=swap)
    waitForHigh = int(blocksbot.getBlockHigh()) + waitingBlocks
    while True:
        try:
            sleep(0.8)
            currentBlock = blocksbot.getBlockHigh()
            if waitForHigh <= currentBlock:
                if checkHoney == True:
                    T = checkIsHoneypot()
                else:
                    T = False
                if T == False:
                    print("\nOK, your Token is not a honeypot!")
                    spinner.stop()
                    buy()
                    break
                else:
                    print("\n",token, "is current a Honeypot Token!")
                    break
        except Exception as e:
            print(e)
            break


def buy():
    spinner = Halo(text='BUY Tokens', spinner='dots')
    spinner.start()
    sleep(0.1)
    try:
        print("\nOK, BUY with", TXN, "Transactions, Good luck")
        for i in range(TXN):
            try:
                bot = Txn_bot(token_address=token, quantity=SNIPEquantity, slippage=slippage, gas_price=gas_price, swap=swap)
                tx = bot.buy_token()
                print(tx[1])
                if tx[0] == False:
                    exit()
            except Exception as e:
                print(e)
        spinner.stop()
        if tx[0] == True:
            if profit != 0:
                checkProfit()
    except Exception as e:
        print(e)
    

def Snip():
    spinner = Halo(text='Waiting for Liquidity', spinner='dots')
    spinner.start()
    sbot = Txn_bot(token_address=token, quantity=SNIPEquantity, slippage=slippage, gas_price=gas_price, swap=swap)
    while True:
        sleep(Timer)
        try:
            print(f"\nMin Output from {SNIPEquantity} BNB:",sbot.amountsOut_buy()[1] / (10 ** sbot.get_token_decimals()))
            try:
                spinner.stop()
                waitBlocks()
                break
            except Exception as e:
                print(e)
                break
        except:
            break
    
Snip()
print("Bot Finish!")