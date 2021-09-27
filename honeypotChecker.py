import requests, json

class HoneyPotChecker():
    def __init__(self, Token_Address):
        self.url = f"https://ishoneypot.trading-tigers.com/token/{Token_Address}"
        
    def Is_Honeypot(self):
        r = requests.get(self.url)
        jres = json.loads(r.text)
        if jres['HONEYPOT']  == False:
            return False
        elif jres['HONEYPOT'] == True:
            return True

    def getSellTAX(self):
        r = requests.get(self.url)
        jres = json.loads(r.text)
        return jres['SELLTAX']

    def getBUYTAX(self):
        r = requests.get(self.url)
        jres = json.loads(r.text)
        return jres['BUYTAX']