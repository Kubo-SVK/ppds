from fei.ppds import Thread, print
from fei.ppds.sync import Semaphore, Event


"""
Objekt Semaphore(0) je mozne nahradit za Event() vice versa
"""
class SharedData():
    def __init__(self, N):
        self.N = N  # pocet vlakien, ktore sa spustaju
        self.arr = [0,1] + [0] * (N)  # inicializacia pola na [0,1,0,0,...]
        self.sig = []  # pole pre semafory/eventy
        for _ in range(self.N-1):
            obj = Semaphore(0)   
            self.sig.append(obj)
        # self.sig[0].signal()  # spusti 1. vlakno
        
    

def compute_fibonacci(fib, i):  
    if(i>0):  # vlakno 0 nema predchodcu so semaforom
        fib.sig[i-1].wait()  # pocka na signal z predchaczajuceho semaforu
    fib.arr[i+2] = fib.arr[i]+fib.arr[i+1]  # zapise cislo do zdielaneho pola
    if(i < fib.N-1):  # posledne vlakno uz nema co nastavovat, kedze nema semafor
        fib.sig[i].signal()  # nastavi svoj semafor, aby sa odblokovalo nasledujuce vlakno


threads = list()
fib = SharedData(100)
    
for i in range(fib.N):
    threads.append(Thread(compute_fibonacci, fib, i))

for t in threads:
    t.join()    


print(fib.arr)

for i in range(2, len(fib.arr)):  # kontrola synchronizacie
    if(fib.arr[i] != fib.arr[i-2]+fib.arr[i-1]):
        print("Chyba v synchronizacii")
        break