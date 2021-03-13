from fei.ppds import Semaphore, Event, Thread, Mutex, print
from time import sleep
from random import randint


class Lightswitch():
    def __init__(self):
        self.mutex = Mutex()
        self.count = 0

    def lock(self, sem):
        self.mutex.lock()
        self.count += 1
        if self.count == 1:
            sem.wait()
        self.mutex.unlock()
        return self.count

    def unlock(self, sem):
        self.mutex.lock()
        self.count -= 1
        if self.count == 0:
            sem.signal()
        self.mutex.unlock()


def init():
    accessData = Semaphore(1)
    turniket = Semaphore(1)
    ls_monitor = Lightswitch()
    ls_cidlo = Lightswitch()
    validData = Semaphore()
    threads = list()
 
 
    for monitor_id in range(8):
        threads.append(Thread(monitor, monitor_id, turniket, validData, ls_monitor, accessData))
    for cidlo_id in range(2):
        threads.append(Thread(cidlo, cidlo_id, turniket, validData, ls_cidlo, accessData, [10, 20]))
    threads.append(Thread(cidlo, 2, turniket, validData, ls_cidlo, accessData, [20, 25]))
        
    for th in threads:
        th.join()
 
def monitor(monitor_id, turniket, validData,ls_monitor, accessData):
    validData.wait()
 
    while True:
        sleep(0.5)
 
        turniket.wait()
        sleep(randint(40, 50) / 1000)
        pocet_citajucich_monitorov = ls_monitor.lock(accessData)
        turniket.signal()
 
        print(f'monit "{monitor_id:02d}": pocet_citajucich_monitorov={pocet_citajucich_monitorov:02d}')
        ls_monitor.unlock(accessData)
 
def cidlo(cidlo_id, turniket, validData, ls_cidlo, accessData, wr):
    while True:
        sleep(randint(50, 60) / 1000)
        
        turniket.wait()
        turniket.signal()
 
        pocet_zapisujucich_cidiel = ls_cidlo.lock(accessData)
        trvanie_zapisu = randint(wr[0], wr[1])/1000
        
        print(f'cidlo "{cidlo_id:02d}":  pocet_zapisujucich_cidiel={pocet_zapisujucich_cidiel:02d}, trvanie_zapisu={trvanie_zapisu:0.3f}')
        sleep(trvanie_zapisu)
        validData.signal()
        ls_cidlo.unlock(accessData)
 
init()
 