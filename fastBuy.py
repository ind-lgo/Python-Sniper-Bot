from txns import Txn_bot
from honeypotChecker import HoneyPotChecker
import argparse, math
from halo import Halo
from time import sleep
spinneroptions = {'interval': 250,'frames': ['🚀 ', '🌙 ', '🚀 ', '🌕 ', '💸 ']}


parser = argparse.ArgumentParser(description='Set your Token and Amount example: "sniper.py -t 0xc87b88aafb95f0b88c3a74fc96344e4bccab6bde -a 0.2 -s 15"')
parser.add_argument('-t', '--token', help='str, Token for snipe e.g. "-t 0xc87b88aafb95f0b88c3a74fc96344e4bccab6bde"')
parser.add_argument('-a', '--amount', help='float, Amount in Bnb to snipe e.g. "-a 0.1"')
parser.add_argument('-s', '--slippage', help='int, slippage in % "-s 10"')
parser.add_argument('-hp', '--honeypot', default=True, nargs="?", const=True, type=bool, help='bool, check if your token to buy is a Honeypot')
parser.add_argument('-swap', '--swap', default=[1], type=list, help='list, Witch Swap? e.g. "-swap [1] for Panackeswap"')
parser.add_argument('-tx', '--txamount', default=1, nargs="?", const=1, type=int, help='int, how mutch tx you want to send? It Split your BNB Amount in e.g. "-tx 5"')
parser.add_argument('-tp', '--takeprofit', default=0, nargs="?", const=True, type=int, help='int, Percentage TakeProfit from your input BNB amount, if 0 then not used. e.g. "-tp 50" ')
args = parser.parse_args()

TXN = int(args.txamount)
quantity = (float(args.amount) / TXN)
slippage = int(args.slippage)
checkHoney = bool(args.honeypot)
gas_price = 6 * (10**9) 
swap = list(args.swap)
token_address = str(args.token)
TXN = int(args.txamount)
takeprofit = int(args.takeprofit)


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
    a = ((quantity * TXN) * takeprofit) / 100
    b = a + (quantity * TXN)
    return b 

profit = "not activated"
if takeprofit != 0: 
    profit = calcProfitExit() 
else:
    profit = 0
del TIGS, TIGSBALANCE

print("Start FastBuy with following arguments")
print("---------------------------------------------------")
print("Amount for Buy:", str(args.amount) , "BNB")
print("Token to Snipe :", args.token)
print("Slippage :", str(args.slippage) + "%")
print("Transaction to send:", str(args.txamount))
print("Amount per transaction :", str(quantity))
print("Take Profit Percent :", str(takeprofit))
print("Min Output from Take Profit:",str(profit))
print("---------------------------------------------------")


def checkProfit():
    spinner = Halo(text='Checking Profit', spinner=spinneroptions)
    spinner.start()
    pbot = Txn_bot(
                    token_address=token_address,
                    quantity=quantity,
                    slippage=slippage,
                    gas_price=gas_price,
                    swap=swap
                    )
    txn = pbot.approve()
    print(txn[1])
    sleep(3)
    tq = math.floor(pbot.get_token_balance()* 10000000)/10000000.0
    cbot = Txn_bot(
                    token_address=token_address,
                    quantity=tq,
                    slippage=slippage,
                    gas_price=gas_price,
                    swap=swap
                    )
    sleep(3)
    spinner.stop()
    while True:
        try:
            sleep(Timer)
            currentProfit = (cbot.amountsOut_sell()[1] /(10**18))
            print("Current Min Output from your Tokens", round(currentProfit,4), end="\r")
            if currentProfit >= profit:
                print("Profit reached, Sell now all Tokens.")
                sbot = Txn_bot(
                    token_address=token_address,
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


if checkHoney == True:
    isHoneypot = HoneyPotChecker(Token_Address=token_address).Is_Honeypot()
    if isHoneypot == False:
        BUY = True
if checkHoney == False:
    BUY = True


if BUY == True:
    for i in range(TXN):
        bot = Txn_bot(token_address=token_address, quantity=quantity, slippage=slippage,gas_price=gas_price,swap=swap)
        tx = bot.buy_token()
        print(tx[1])
    if tx[0] == True:
        if profit != 0:
            checkProfit()
else:
    print("Token is Hoooneypooot!")
