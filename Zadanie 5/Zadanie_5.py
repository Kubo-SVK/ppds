from fei.ppds import Semaphore, Mutex, Thread, print
from random import randint
from time import sleep
 
"""M a N su parametre modelu, nie synchronizacie ako takej.
Preto ich nedavame do zdielaneho objektu.
    M - pocet porcii misionara, ktore sa zmestia do hrnca.
    N - pocet divochov v kmeni (kuchara nepocitame).
    C - pocet kucharov
"""
M = 10
N = 5
C = 3
 
 
class SimpleBarrier:
    def __init__(self, N):
        self.N = N
        self.mutex = Mutex()
        self.cnt = 0
        self.sem = Semaphore(0)
 
    def wait(self,
             print_str,
             savage_id,
             print_last_thread=False,
             print_each_thread=False):
        self.mutex.lock()
        self.cnt += 1
        if print_each_thread:
            print(print_str % (savage_id, self.cnt))
        if self.cnt == self.N:
            self.cnt = 0
            if print_last_thread:
                print(print_str % (savage_id))
            self.sem.signal(self.N)
        self.mutex.unlock()
        self.sem.wait()
 
 
class Shared:
    def __init__(self):
        self.mutex = Mutex()
        self.cooking = Mutex()
        self.refill = Mutex()
        self.servings = 0
        self.active_cooks = 0
        self.cooks_done = 0
        self.full_pot = Semaphore(0)
        self.empty_pot = Semaphore(0)
        self.barrier1 = SimpleBarrier(N)
        self.barrier2 = SimpleBarrier(N)
        self.pot_ready = Semaphore(0)
 
 
def get_serving_from_pot(savage_id, shared):
    print("divoch %2d: beriem si porciu" % savage_id)
    shared.servings -= 1
 
 
def eat(savage_id):
    print("divoch %2d: hodujem" % savage_id)
    # Zjedenie porcie misionara nieco trva...
    sleep(0.2 + randint(0, 3) / 10)
 
 
def savage(savage_id, C, shared):
    while True:

        shared.barrier1.wait(
            "divoch %2d: prisiel som na veceru, uz nas je %2d",
            savage_id,
            print_each_thread=True)
        shared.barrier2.wait("divoch %2d: uz sme vsetci, zaciname vecerat",
                             savage_id,
                             print_last_thread=True)
 
        # Nasleduje klasicke riesenie problemu hodujucich divochov.
        shared.mutex.lock()
        print("divoch %2d: pocet zostavajucich porcii v hrnci je %2d" %
              (savage_id, shared.servings))
        if shared.servings == 0:
            print(f'divoch {savage_id:2d} budim {C:2d} kucharov')
            shared.empty_pot.signal(C)
            shared.full_pot.wait()
        get_serving_from_pot(savage_id, shared)
        shared.mutex.unlock()
 
        eat(savage_id)
 
 
def put_servings_in_pot(id, M, shared): 
    while True:
        shared.cooking.lock()
        if(shared.active_cooks == M):
            shared.cooking.unlock()
            return
        shared.active_cooks += 1
        shared.cooking.unlock()
        print(f'kuchar {id}: varim')
        # navarenie jedla tiez cosi trva...
        sleep(0.4 + randint(0, 2) / 10)
        shared.servings += 1
 
 
def cook(id, M, C, shared):
    while True:
        shared.empty_pot.wait()
        put_servings_in_pot(id, M, shared)
        
        shared.refill.lock()
        print(f'kuchar {id}: hotovo')
        shared.cooks_done += 1
        if(shared.cooks_done == C):
            shared.active_cooks = 0
            shared.cooks_done = 0
            shared.full_pot.signal()
        shared.refill.unlock()
 
 
def init_and_run(N, M, C):
    threads = list()
    shared = Shared()
    for savage_id in range(0, N):
        threads.append(Thread(savage, savage_id, C, shared))
    
    for cook_id in range(0, C):
        threads.append(Thread(cook, cook_id, M, C, shared))
 
    for t in threads:
        t.join()
 
 
if __name__ == "__main__":
    init_and_run(N, M, C)
