from fei.ppds import Thread, Mutex, Semaphore
from time import sleep
from random import randint


class SimpleBarrier():
    def __init__(self, N):
        self.mutex = Mutex()
        self.capacity = N
        self.counter = 0
        self.sem = Semaphore()

    def wait(self):
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.capacity:
            print(f'Lod zakotvila s posadkou {self.counter} ludi')
            self.counter = 0
            self.sem.signal(self.capacity)
        self.mutex.unlock()
        self.sem.wait()


class Shared():
    def __init__(self):
        self.mutex = Mutex()
        self.dealersQ = Semaphore()
        self.officersQ = Semaphore()
        self.officerCounter = 0
        self.dealerCounter = 0
        self.barrier = SimpleBarrier(4)


def sail(sh: Shared, cpt: bool):
    sh.barrier.wait()
    if cpt:
        sleep(randint(2, 10)/10)
        sh.mutex.unlock()


def officer(sh: Shared, id: int):
    while True:
        isCaptain = False

        sh.mutex.lock()
        sh.officerCounter += 1

        if sh.officerCounter == 4:
            sh.officerCounter -= 4
            sh.officersQ.signal(4)
            isCaptain = True

        elif sh.officerCounter == 2 and sh.dealerCounter >= 2:
            sh.officerCounter -= 2
            sh.dealerCounter -= 2
            sh.officersQ.signal(2)
            sh.dealersQ.signal(2)
            isCaptain = True

        else:
            sh.mutex.unlock()

        sh.officersQ.wait()
        print(f'Straznik {id} nastupuje na lod')
        sail(sh, isCaptain)


def dealer(sh: Shared, id: int):
    while True:
        isCaptain = False

        sh.mutex.lock()
        sh.dealerCounter += 1

        if sh.dealerCounter == 4:
            sh.dealerCounter -= 4
            sh.dealersQ.signal(4)
            isCaptain = True

        elif sh.officerCounter == 2 and sh.dealerCounter >= 2:
            sh.officerCounter -= 2
            sh.dealerCounter -= 2
            sh.officersQ.signal(2)
            sh.dealersQ.signal(2)
            isCaptain = True

        else:
            sh.mutex.unlock()

        sh.dealersQ.wait()
        print(f'Dealer {id} nastupuje na lod')
        sail(sh, isCaptain)


threads = []
sh = Shared()

officers = 10
dealers = 10

for i in range(officers):
    threads.append(Thread(officer, sh, i))

for i in range(dealers):
    threads.append(Thread(dealer, sh, i))
