from fei.ppds import Semaphore, Thread, Mutex, Event
from time import sleep
import time
from random import randint


class LS():
    def __init__(self, semaphore):
        self.mutex = Mutex()
        self.sem = semaphore
        self.count = 0

    def lock(self):
        self.mutex.lock()
        self.count += 1
        if self.count == 1:
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
        self.worklog = list()
        self.stop = False


def reader(sh, range, i):
    while True:
        if sh.stop:
            break

        sleep(randint(0, 10)/10)
        sh.ls.lock()
        time = randint(range[0], range[1])/10
        sleep(time)
        print(f'Reader {i} odchadza z miestnosti')
        sh.ls.unlock()


def writer(sh, range, i):
    while True:
        if sh.stop:
            break

        sleep(randint(0, 10)/10)
        sh.sem.wait()
        time = randint(range[0], range[1])/10
        sleep(time)
        print(f'Writer {i} odchadza z miestnosti')
        sh.sem.signal()


readers_count = 10  # pocet citatelov
writers_count = 10  # pocet zapisovatelov
reading_time = (0, 5)  # rozsha od - do pre generator nahodnych cisiel
writing_time = (0, 10)
run_time = 10  # dlzka zivotnosti vlakien v sekundach

sh = Shared()
threads = list()


for i in range(writers_count):
    threads.append(Thread(writer, sh, writing_time, i))

for i in range(readers_count):
    threads.append(Thread(reader, sh, reading_time, i))

start = time.time()
while (time.time() - start) < run_time: 
    pass

sh.stop = True

for i in threads:
    i.join()
