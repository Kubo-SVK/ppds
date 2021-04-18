import requests
from time import time

CURRENCY = "EUR"
URL = "https://api.exchangerate.host/latest?base={cur}&source=crypto&symbols={sym}"

class SharedData():
    def __init__(self):
        self.data = list()
        
    def append(self, data):
        self.data.append(data)
        
        
    def __str__(self):
        out = ""
        for i in self.data:
            out += i[0]+ "/" + CURRENCY + ":" + " " + i[1] + "\n"
        return out


def gatherTradeData(data: SharedData, symbol: str):
    req_url = URL.format(cur=CURRENCY, sym=symbol)
    
    response = requests.get(req_url)
    rates = response.json()['rates']
    
    if len(rates) == 1:
        data.append([symbol, str(rates[symbol])])
    else:
        data.append([symbol, "unsupported"])


def main():
    crypto_cur = list()
    data = SharedData()
    
    with open("crypto.txt","r") as file:
        for line in file:
            crypto_cur.append(line.strip())
    
    start = time()
    for symbol in crypto_cur:
        gatherTradeData(data, symbol)
    duration = time() - start
        
    print(data)
    print(f'\nExectution time: {duration}')

if __name__ == "__main__":
    main()