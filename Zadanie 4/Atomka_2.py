from fei.ppds import Semaphore, Event, Thread, Mutex, print
from time import sleep
from random import randint


class Barrier():
    def __init__(self, n):
        self.mutex = Mutex()
        self.event = Event()
        self.counter = n
        self.n = n
        
    def wait(self):
        self.mutex.lock()
        self.counter -= 1
        if(self.counter == 0):
            self.counter = self.n
            self.event.signal()
            self.mutex.unlock()
            return
        self.mutex.unlock()
        self.event.wait()
    
    
class Lightswitch():
    def __init__(self):
        self.mutex = Mutex()
        self.count = 0

    def lock(self, sem):
        self.mutex.lock()
        counter = self.count
        self.count += 1
        if self.count == 1:
            sem.wait()
        self.mutex.unlock()
        return counter

    def unlock(self, sem):
        self.mutex.lock()
        self.count -= 1
        if self.count == 0:
            sem.signal()
        self.mutex.unlock()


def init(x):
    accessData = Semaphore(1)
    turniket = Semaphore(1)
    ls_monitor = Lightswitch()
    ls_cidlo = Lightswitch()
    validData = Event()
    barrier_1= Barrier(x)
    barrier_2= Barrier(x)
    
    for monitor_id in range(x):
        Thread(monitor, monitor_id, turniket, validData, ls_monitor, accessData, barrier_1, barrier_2)
    for cidlo_id in range(2):
        Thread(cidlo, cidlo_id, turniket, validData, ls_cidlo, accessData, [10, 20])
    Thread(cidlo, 2, turniket, validData, ls_cidlo, accessData, [20, 25])
 
def monitor(monitor_id, turniket, validData,ls_monitor, accessData, bar1, bar2):
    validData.wait()
    while True:
        bar1.wait()
        sleep(0.5)
 
        turniket.wait()
        sleep(randint(40, 50) / 1000)
        pocet_citajucich_monitorov = ls_monitor.lock(accessData)
        turniket.signal()
        print(f'monit "{monitor_id:02d}": pocet_citajucich_monitorov={pocet_citajucich_monitorov:02d}')
        ls_monitor.unlock(accessData)
        bar2.wait()

 
def cidlo(cidlo_id, turniket, validData, ls_cidlo, accessData, wr):
    while True:
        sleep(randint(50, 60) / 1000)
        
        turniket.wait()
        turniket.signal()
 
        pocet_zapisujucich_cidiel = ls_cidlo.lock(accessData)
        trvanie_zapisu = randint(wr[0], wr[1])/1000
        sleep(trvanie_zapisu)
        print(f'cidlo "{cidlo_id:02d}":  pocet_zapisujucich_cidiel={pocet_zapisujucich_cidiel:02d}, trvanie_zapisu={trvanie_zapisu:0.3f}')

        ls_cidlo.unlock(accessData)

        if(pocet_zapisujucich_cidiel == 2):
            validData.signal()
 
 
monitor_count = 8
 
init(monitor_count)
 