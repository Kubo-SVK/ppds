# Zadanie 7

Vytvoril som plánovač, ktorý prideľuje procesorový čas pre 4 koporgramy. V riešení som sa pokúšal použiť, čo najviac funkcíí a obsluhy výnimiek.

## Plánovač
Objekt plánovača, drží zoznam koprogramov, ktoré čakajú na spustenie. Tento zoznam je implementovaný ako klasický List.
```python
def __init__(self):
        self.tasks = list()
```
Plánovač obsahuje aj metódy na obsluhu:

1) Pridávanie koprogramov, ktoré zabezpečí, aby pri spustení už koprogram čakal na prvom volaní funkcie yield.
```python
def add(self, task):
        next(task)
        self.tasks.append(task)
```
2) Obsluha behu programov. Koprogramy sa striedajú v nekonečnej slučke, pokým niektorý z nich nevyvolá výnimku. V tom prípade plánovač ukončí každý koprogram volaním funkcie close().
```python
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
```

## Koprogramy
1) Generuje náhodné čísla a kontroluje, či už bola prekročená hraničná hodnota.

```python
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
```

2) Kontroluje, či bolo vygenerované číslo párne/nepárne a vedie ich štatistiku.
```python
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
```

3) Upraví hodnotu vygenerovaného čísla o náhodnú hodnotu a pričíta k súčtu predchádzajúcich.

```python
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
```

4) Na obrazovku vypisuje každých ~100ms aktuálnu hodnotu súčtu. (Pokus o simuláciu Sleep(0.1))
```python
def reminder():
    val = 0
    start = time()
    while True:
        val = (yield val)
        cur = time()
        if cur-start > 0.1:
            start = cur
            print(f'Priebezny sucet hodnot: {val}')
```