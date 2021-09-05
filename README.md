# Pancakeswap_BSC_Sniper_Bot
![alt text](https://trading-tigers.com/assets/img/TradingTigers.png)  
Web3 Pancakeswap Sniper bot written in python3, Please note the license conditions!  
The first Binance Smart Chain sniper bot with Honeypot checker.  
# Infos
If you have 100 Tigs on your BSC address, the bot will check for liquidity every 0.1 seconds, if you have less than 100 TIGS then only every 5 seconds!  
If you are not familiar with Python please have a look at Releases!  

# [TradingTigers Token @BSC](https://bscscan.com/token/0x34faa80fec0233e045ed4737cc152a71e490e2e3)  
  
Setup your Address and secret key in keys.py 

Install in Python:
```python
python3 -m pip install -r requirements.txt
```
Start Sniper:  
```python
python3 Sniper.py -t <TOKEN_ADDRESS> -a <AMOUNT> -s <SLIPPAGE> -tx <TXAMOUNT>
python3 Sniper.py -t 0x34faa80fec0233e045ed4737cc152a71e490e2e3 -a 0.1 -s 20 -tx 3
```  
Here are all options:
```python
'-t', '--token', help='str, Token for snipe e.g. "-t 0xc87b88aafb95f0b88c3a74fc96344e4bccab6bde"')
'-a', '--amount', help='float, Amount in Bnb to snipe e.g. "-a 0.1"')
'-s', '--slippage', default=10, nargs="?", const=1, type=int, help='int, slippage in % "-s 10"')
'-tx', '--txamount', default=1, nargs="?", const=1, type=int, help='int, how mutch tx you want to send? Its Splitt your BNB Amount. e.g. "-tx 5"')
'-swap', '--swap', default=[1], type=list, help='list, Witch Swap? e.g. "-swap [1]" for Panackeswap')
'-hp', '--honeypot', default=True, nargs="?", const=True, type=bool, help='bool, check if your token to buy is a Honeypot')
```