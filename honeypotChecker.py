from requests_html import HTMLSession
import time 


class HoneyPotChecker():

    def __init__(self, Token_Address):
        self.url = f"https://ishoneypot.trading-tigers.com/?address={Token_Address}"
        self.session = HTMLSession()
        self.Honeypot = True

    def Is_Honeypot(self):
        r = self.session.get(self.url)
        r.html.render(sleep=0.5, keep_page=True)
        p = r.html.xpath('//*[@id="checktoken"]/div')[0].text
        if "Does not seem like a honeypot." in p:
            return False
        else:
            self.Honeypot = True
            return self.Honeypot
