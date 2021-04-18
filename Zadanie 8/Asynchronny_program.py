import aiohttp
from time import time
import asyncio

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

async def task(name: str, data: SharedData, queue: asyncio.Queue):
    async with aiohttp.ClientSession() as session:
        while not queue.empty():
            sym = await queue.get()
            url = URL.format(cur=CURRENCY, sym=sym)
            print(f"Task {name} getting data for: {sym}")
            async with session.get(url) as response:
                rates = await response.json()
                rates = rates['rates']
                if len(rates) == 1:
                    data.append([sym, str(rates[sym])])
                else:
                    data.append([sym, "unsupported"])

async def main():
    data = SharedData()
    crypto_queue = asyncio.Queue()
    
    with open("crypto.txt","r") as file:
        for line in file:
            await crypto_queue.put(line.strip())
            
    start = time()    
    await asyncio.gather(
        task("Task 1", data, crypto_queue),
        task("Task 2", data, crypto_queue),
        task("Task 2", data, crypto_queue)
    )
    duration = time() - start
    
    print(data)

    print(f'Async execution time: {duration}')
    
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
    