
from txns import Txn_bot
from time import sleep
import argparse
from honeypotChecker import HoneyPotChecker
from halo import Halo
from threading import Thread


gas_price = 6 * (10**9)
swap = [1]
TIGS = Txn_bot(token_address="0x34faa80fec0233e045ed4737cc152a71e490e2e3", quantity=0, slippage=0, gas_price=gas_price, swap=swap)
TIGSBALANCE = TIGS.get_token_balance()
print("")
print("")
if TIGSBALANCE >= 100:
    Time = 0.1
    print("Welcome Premium Tiger!\nSet Checktime to " + str(Time) + " seconds")
else:
    Time = 5
    print("Welcome Tiger Buy 100TIGS to get faster checktime.\nSet Checktime to " + str(Time) + " seconds")
del TIGS, TIGSBALANCE


parser = argparse.ArgumentParser(description='Set your Token and Amount example: "sniper.py -t 0xc87b88aafb95f0b88c3a74fc96344e4bccab6bde -a 0.2 -s 15"')
parser.add_argument('-t', '--token', help='str, Token for snipe e.g. "-t 0xc87b88aafb95f0b88c3a74fc96344e4bccab6bde"')
parser.add_argument('-a', '--amount', help='float, Amount in Bnb to snipe e.g. "-a 0.1"')
parser.add_argument('-s', '--slippage', default=10, nargs="?", const=1, type=int, help='int, slippage in % "-s 10"')
parser.add_argument('-tx', '--txamount', default=1, nargs="?", const=1, type=int, help='int, how mutch tx you want to send? It Split your BNB Amount in e.g. "-tx 5"')
parser.add_argument('-swap', '--swap', default=[1], type=list, help='list, Witch Swap? e.g. "-swap [1] for Panackeswap"')
parser.add_argument('-hp', '--honeypot', default=True, nargs="?", const=True, type=bool, help='bool, check if your token to buy is a Honeypot')
args = parser.parse_args()


TXN = int(args.txamount)
SNIPEquantity = (float(args.amount) / TXN)
slippage = int(args.slippage)
token=args.token
checkHoney = args.honeypot
Timer = float(Time)

print("")
print("Start Sniper with following arguments")
print("------------------------------------------------------------------------------")
print("Amount for Buy:", str(args.amount) , "BNB")
print("Token to Snipe :", args.token)
print("Slippage :", str(args.slippage) + "%")
print("Transaction to send:", str(args.txamount))
print("Amount per transaction :", str(SNIPEquantity))
print("------------------------------------------------------------------------------")


def checkIsHoneypot():
    isHoney = HoneyPotChecker(token).Is_Honeypot()
    return isHoney


def buy():
    sleep(0.1)
    print("\nOK, Send", TXN, "Transaction ,Good luck")
    for i in range(TXN):
        try:
            bot = Txn_bot(token_address=token, quantity=SNIPEquantity, slippage=slippage, gas_price=gas_price, swap=swap)
            bot.buy_token()
        except Exception as e:
            print(e)
    

@Halo(text='Waiting for Liquidity', spinner='dots')
def Snip():
    sbot = Txn_bot(token_address=token, quantity=SNIPEquantity, slippage=slippage, gas_price=gas_price, swap=swap)
    while(True):
        sleep(Timer)
        try:
            print(f"\nMin Output from {SNIPEquantity} BNB:",sbot.amountsOut_buy()[1] / (10 ** sbot.get_token_decimals()))
            try:
                if checkHoney == True:
                    T = checkIsHoneypot()
                else:
                    T = False
                if T == False:
                    print("\nOK, your token is no honeypot!")
                    Thread(target=buy,).start()
                    break
                else:
                    print("\n",token, "is Honeypot Token!")
                    break
            except Exception as e:
                print(e)
                break
        except:
            pass


Snip()






