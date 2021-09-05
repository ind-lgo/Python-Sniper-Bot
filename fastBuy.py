from txns import Txn_bot
from honeypotChecker import HoneyPotChecker
import argparse


parser = argparse.ArgumentParser(description='Set your Token and Amount example: "sniper.py -t 0xc87b88aafb95f0b88c3a74fc96344e4bccab6bde -a 0.2 -s 15"')
parser.add_argument('-t', '--token', help='str, Token for snipe e.g. "-t 0xc87b88aafb95f0b88c3a74fc96344e4bccab6bde"')
parser.add_argument('-a', '--amount', help='float, Amount in Bnb to snipe e.g. "-a 0.1"')
parser.add_argument('-s', '--slippage', help='int, slippage in % "-s 10"')
args = parser.parse_args()


quantity = float(args.amount)
slippage = int(args.slippage)
gas_price = 6 * (10**9) 
swap = [1]
token_address=args.token


bot = Txn_bot(
    token_address=token_address,
    token_addressOut=None,
    quantity=quantity,
    slippage=slippage,
    gas_price=gas_price,
    swap=swap)


if HoneyPotChecker(Token_Address=token_address).Is_Honeypot() == False:
    bot.buy_token()
else:
    print("Token is Hoooneypooot!")
