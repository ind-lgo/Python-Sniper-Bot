# Pancakeswap_BSC_Sniper_Bot
![TradingTigers](https://trading-tigers.com/assets/img/TradingTigers.png)  
Web3 Pancakeswap Sniper&& Take Profit bot written in python3, Please note the license conditions!  
### The first Binance Smart Chain sniper bot with Honeypot checker!  
![Sniper](https://trading-tigers.com/assets/img/preview01.png)  
# Infos
If you have 100 Tigs on your BSC address, the bot will check for liquidity every 0.1 seconds,  if you have less than 100 TIGS then only every 5 seconds!  

## [TradingTigers Token @BSC](https://bscscan.com/token/0x34faa80fec0233e045ed4737cc152a71e490e2e3)  
![Sniper](https://trading-tigers.com/assets/img/Gui-Preview01.png)  

# Download
If you are not familiar with Python please have a look at [Releases](https://github.com/Trading-Tiger/Pancakeswap_BSC_Sniper_Bot/releases), there you can download Windows executable.

Setup your Address and secret key in keys.json.
Edit your Start_Sniper.bat or Start_fastBuy.bat, insert your Token Address want to Snipe/Buy!

You don't need Administrator rights!

Here are all options:
```python3
'-t', '--token', Token for snipe e.g. "-t 0xc87b88aafb95f0b88c3a74fc96344e4bccab6bde"
'-a', '--amount', float, Amount in Bnb to snipe e.g. "-a 0.1"
'-s', '--slippage', default=10, slippage in % "-s 10"
'-tx', '--txamount', default=1, how mutch tx you want to send? It Split your BNB Amount in e.g. "-tx 5"
'-swap', '--swap', default=[1], Witch Swap? e.g. "-swap [1]" for Panackeswap
'-hp', '--honeypot', default=True, check if your token to buy is a Honeypot
'-tp', '--takeprofit', default=0,  Percentage TakeProfit from your input BNB amount, if 0 then not used. e.g. "-tp 50" '
'-wb', '--awaitBlocks', default=0, Await Blocks before sending BUY Transaction, if 0 then not used. e.g. "-ab 50" ')
```


# Install Python
First of all, you need install Python3+

```python
python3 -m pip install -r requirements.txt
```  

Start Sniper:  
```python
python3 Sniper.py -t <TOKEN_ADDRESS> -a <AMOUNT> -s <SLIPPAGE> -tx <TXAMOUNT>
python3 Sniper.py -t 0x34faa80fec0233e045ed4737cc152a71e490e2e3 -a 0.1 -s 20 -tx 3
```  

