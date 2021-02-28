from fei.ppds import Thread
from fei.ppds.sync import Mutex
from time import sleep
from random import randint


class Fibonacci():
    def __init__(self, N):
        self.arr = [0,1] + [0] * N
        self.N = N
        self.count = 0
        self.mutex = Mutex()
    
 
def compute_fibonacci(fib, i):
    sleep(randint(1,10)/100)  # vynutene prepnutie
    while True:
        fib.mutex.lock()
        if(fib.count == i):
            fib.arr[i+2] = fib.arr[i+1] + fib.arr[i]
            fib.count += 1
            fib.mutex.unlock()
            break
        fib.mutex.unlock()
 
fib = Fibonacci(20)
threads = list()

for i in range(fib.N):
    threads.append(Thread(compute_fibonacci, fib, i))
    
for t in threads:
    t.join()

print(fib.arr)

for i in range(2, len(fib.arr)):  # kontrola synchronizacie
    if(fib.arr[i] != fib.arr[i-2]+fib.arr[i-1]):
        print("Chyba v synchronizacii")
        break
    