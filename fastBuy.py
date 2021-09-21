from txns import Txn_bot
from honeypotChecker import HoneyPotChecker
import argparse


parser = argparse.ArgumentParser(description='Set your Token and Amount example: "sniper.py -t 0xc87b88aafb95f0b88c3a74fc96344e4bccab6bde -a 0.2 -s 15"')
parser.add_argument('-t', '--token', help='str, Token for snipe e.g. "-t 0xc87b88aafb95f0b88c3a74fc96344e4bccab6bde"')
parser.add_argument('-a', '--amount', help='float, Amount in Bnb to snipe e.g. "-a 0.1"')
parser.add_argument('-s', '--slippage', help='int, slippage in % "-s 10"')
parser.add_argument('-hp', '--honeypot', default=True, nargs="?", const=True, type=bool, help='bool, check if your token to buy is a Honeypot')
parser.add_argument('-swap', '--swap', default=[1], type=list, help='list, Witch Swap? e.g. "-swap [1] for Panackeswap"')
parser.add_argument('-tx', '--txamount', default=1, nargs="?", const=1, type=int, help='int, how mutch tx you want to send? It Split your BNB Amount in e.g. "-tx 5"')
args = parser.parse_args()


quantity = float(args.amount)
slippage = int(args.slippage)
checkHoney = bool(args.honeypot)
gas_price = 6 * (10**9) 
swap = list(args.swap)
token_address = str(args.token)
TXN = int(args.txamount)


if checkHoney == True:
    isHoneypot = HoneyPotChecker(Token_Address=token_address).Is_Honeypot()
    if isHoneypot == False:
        BUY = True
if checkHoney == False:
    BUY = True


if BUY = True:
    quantity = quantity / TXN
    for i in range(TXN):
        bot = Txn_bot(token_address=token_address, quantity=quantity, slippage=slippage,gas_price=gas_price,swap=swap)
        bot.buy_token()
else:
    print("Token is Hoooneypooot!")
