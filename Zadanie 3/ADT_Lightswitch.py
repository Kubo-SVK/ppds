from fei.ppds import Semaphore, Thread, Mutex
from time import sleep
from random import randint

class LS():
    def __init__(self, semaphore):
        self.mutex = Mutex()
        self.sem = semaphore
        self.count = 0
        
    def lock(self):
        self.mutex.lock()
        self.count += 1
        if self.count == 5:
            self.sem.wait()
        self.mutex.unlock()
        
    def unlock(self):
        self.mutex.lock()
        self.count -= 1
        if self.count == 0:
            self.sem.signal()
        self.mutex.unlock()

class Shared():
    def __init__(self):
        self.sem = Semaphore(1)
        self.ls = LS(self.sem)
        
def reader(sh,i):
    sleep(randint(0,10)/10)
    sh.ls.lock()
    print(f'Reader {i} vstupil do miestnosti')
    for j in range(20):
        _ = 2**j
    sh.ls.unlock()
    print(f'Reader {i} odisiel z miestnosti')
    
def writer(sh,i):
    sleep(randint(0,8)/10)
    sh.sem.wait()
    print(f'Writer {i} vstupil do miestnosti')
    for j in range(20):
        _ = 2**j
    sh.sem.signal()
    print(f'Writer {i} odisiel z miestnosti')
        
sh = Shared()
    
threads = list()  

for i in range(20):
    threads.append(Thread(writer, sh, i))
      
for i in range(100):
    threads.append(Thread(reader, sh, i))



for i in threads:
    i.join()
        