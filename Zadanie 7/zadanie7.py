from random import randint
from time import time


class Scheduler():
    def __init__(self):
        self.tasks = list()

    def add(self, task):
        next(task)
        self.tasks.append(task)

    def run(self):
        ret_val = 0
        while True:
            try:
                task = self.tasks.pop(0)
                ret_val = task.send(ret_val)
                self.tasks.append(task)
            except StopIteration:
                print("-"*10 + "STATS" + "-"*10)
                for i in self.tasks:
                    i.close()
                break


def gen_number(stop):
    bound = 0
    num = 0
    while True:
        bound = (yield num)
        if bound > stop:
            print("-"*25)
            print(f'KONIEC - Sucet {bound} prekrocil hranicu {stop}')
            break
        num = randint(0, 50)
        print(f'Generujem {num}')


def check_even():
    num = 0
    odd = 0
    even = 0
    while True:
        try:
            num = (yield num)
            if num % 2 == 0:
                even += 1
                print(f'Cislo {num} je parne')
            else:
                odd += 1
                print(f'Cislo {num} je neparne')
        except GeneratorExit:
            print(f'Pocet parnych: {even}')
            print(f'Pocet neparnych: {odd}')
            print(f'Celkovy pocet vygenerovanych cisiel {even+odd}')
            return


def correction():
    bound = 0
    val_sum = 0
    while True:
        try:
            bound += (yield bound)
            salt = randint(-10, 10)
            print(f'Korekcia hodnotou {salt}')
            bound += salt
            val_sum += salt
        except GeneratorExit:
            print(f'Sucet vsetkych korekcii {val_sum}')
            return


def reminder():
    val = 0
    start = time()
    while True:
        val = (yield val)
        cur = time()
        if cur-start > 0.1:
            start = cur
            print(f'Priebezny sucet hodnot: {val}')


stop_value = 50000

scheduler = Scheduler()
scheduler.add(gen_number(stop_value))
scheduler.add(check_even())
scheduler.add(correction())
scheduler.add(reminder())
scheduler.run()
