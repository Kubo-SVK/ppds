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
    validData = Event()
    threads = list()
 
 
    for monitor_id in range(2):
        threads.append(Thread(monitor, monitor_id, turniket, validData, ls_monitor, accessData))
    for cidlo_id in range(11):
        threads.append(Thread(cidlo, cidlo_id, turniket, validData, ls_cidlo, accessData))
        
    for th in threads:
        th.join()
 
def monitor(monitor_id, turniket, validData,ls_monitor, accessData):
    # monitor nemôže pracovať, kým nie je aspoň 1 platný údaj v úložisku
    validData.wait()
 
    while True:
        # monitor má prestávku 500 ms od zapnutia alebo poslednej aktualizácie
        sleep(0.5)
 
        # zablokujeme turniket, aby sme vyhodili čidlá z KO
        turniket.wait()
            # získame prístup k úložisku
        pocet_citajucich_monitorov = ls_monitor.lock(accessData)
        turniket.signal()
 
        # prístup k údajom simulovaný nasledovným výpisom
        print(f'monitor "{monitor_id}": pocet_citajucich_monitorov={pocet_citajucich_monitorov}')
        # aktualizovali sme údaje, odchádzame z úložiska
        ls_monitor.unlock(accessData)
 
def cidlo(cidlo_id, turniket, validData, ls_cidlo, accessData):
    while True:
        # čidlá prechádzajú cez turniket, pokým ho nezamkne monitor
        turniket.wait()
        turniket.signal()
 
        # získame prístup k úložisku
        pocet_zapisujucich_cidiel = ls_cidlo.lock(accessData)
        # prístup k údajom simulovaný čakaním v intervale 10 až 15 ms
        # podľa špecifikácie zadania informujeme o čidle a zápise, ktorý ide vykonať
        trvanie_zapisu = randint(10, 15)/1000
        
        print(f'cidlo "{cidlo_id}":  pocet_zapisujucich_cidiel={pocet_zapisujucich_cidiel}, trvanie_zapisu={trvanie_zapisu:.3f}')
        sleep(trvanie_zapisu)
        # po zapísaní údajov signalizujeme, že údaj je platný
        validData.signal()
        # a odchádzame z úložiska preč
        ls_cidlo.unlock(accessData)
 
init()
 