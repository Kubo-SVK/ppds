from fei.ppds import Thread, print
from fei.ppds.sync import Semaphore, Mutex, Event

class Fibonacci():
    def __init__(self, N):
        self.N = N
        self.arr = [0,1] + [0] * (N)
        self.th_count = 0
        self.count = 0
        self.mutex = Mutex()
        self.turnstile = Semaphore(0)  # moze sa nahradit za Event()
        
        self.arr[1] = 1
    
    def wait(self):
        self.mutex.lock()
        self.th_count += 1
        if(self.th_count == self.N):
            self.signal()
        self.mutex.unlock()
        self.turnstile.wait()
    
    def signal(self):
        if(isinstance(self.turnstile, Event)):
            self.turnstile.signal()
        else:
            for _ in range(self.N):
                self.turnstile.signal()
        
        self.th_count = 0
    
 
def compute_fibonacci(fib, i):    
    while True:
        fib.wait()
        if(fib.count == i):
            fib.arr[i+2] = fib.arr[i+1] + fib.arr[i]
            fib.count += 1
            fib.N -= 1
            fib.signal()
            print(f'Zostavajucich vlakien: {fib.N}')
            break
        

fib = Fibonacci(10)
threads = list()

for i in range(fib.N):
    threads.append(Thread(compute_fibonacci, fib, i))
    
for t in threads:
    t.join()

print(fib.arr)

for i in range(2, len(fib.arr)):
    if(fib.arr[i] != fib.arr[i-2]+fib.arr[i-1]):
        print("Chyba v synchronizacii")
        break