# Zadanie 2

Implementácia Fibonacciho postupnosti pomocou vlákien.

---
## Fibonacci_Bariera.py
---
```Python
def compute_fibonacci(fib, i):
    sleep(randint(1,10)/100)  # vynutene prepnutie
    while True:
        fib.mutex.lock()
        if(fib.count == i):
            fib.arr[i+2] = fib.arr[i+1] + fib.arr[i]
            fib.count += 1
            fib.mutex.unlock()
            break
        fib.mutex.unlock()
```
Implementácia pomocou bariery.

---
## Fibonacci_Mutex.py

```Python
def compute_fibonacci(fib, i):
    sleep(randint(1,10)/100) # vynutene prepnutie
    while True:
        fib.mutex.lock()
        if(fib.count == i):
            fib.arr[i+2] = fib.arr[i+1] + fib.arr[i]
            fib.count += 1
            fib.mutex.unlock()
            break
        fib.mutex.unlock()
```
Vlákna bežia v nekonečnom cykle a postupne zapisujú do poľa. Po zapísaní sa vlákno ukonči. Mutex sa využíva práve kvôli prístupu do poľa.

---
## Fibonacci_Semafory.py

```python
def compute_fibonacci(fib, i):  
    if(i>0):  # vlakno 0 nema predchodcu so semaforom
        fib.sig[i-1].wait()  # pocka na signal z predchaczajuceho semaforu
    fib.arr[i+2] = fib.arr[i]+fib.arr[i+1]  # zapise cislo do zdielaneho pola
    if(i < fib.N-1):  # posledne vlakno uz nema co nastavovat, kedze nema semafor
        fib.sig[i].signal()  # nastavi svoj semafor, aby sa odblokovalo nasledujuce vlakno
```
Z môjho pohľadu najoptimálnejší spôsob, ako túto úlohu vykonať. Každé vlákno má svôj semafór/udalosť, ktorú odblokováva vlákno predchádzajúce.

---
## Otázky

1) Aký je najmenší počet synchronizačných objektov (semafory, mutexy, udalosti) potrebných na riešenie tejto úlohy?
2) Ktoré z prebratých synchronizačných vzorov (vzájomné vylúčenie, signalizácia, rendezvous, bariéra) sa dajú (rozumne) využiť pri riešení tejto úlohy? Konkrétne popíšte, ako sa ten-ktorý synchronizačný vzor využíva vo vašom riešení.

Odpovede:  
1)  a) **Semafóry** -Najmenej sa mi podarilo dosiahnuť N-1 semaforov/udalostí, keďze vlákno 0 nemusí čakať na predchádzajúce a posledné už nemá komu predať informáciu. Pri tomto riešení netreba žiaden Mutex, keďze vlákno nastavuje semafór/udalosť až po zapísaní do poľa.  
b) **Bariera** - Pri riešení s barierou som potreboval 1 barieru, 1 semafór/udalosť a Mutex. Mutex bráni viacnásobnému prístupu, pri k počítadlu pri implementácii bariery a semafor ju blokuje/otvára. Samotné riešenie si už vyžiadalo len 1 takúto barieru.

2)  a) **Semafóry** - Pri použití výhradne semafórov/udalostí si vlákno kontroluje semafór/udalosť predchádzajúceho vlákna.  
 b) **Bariera** - Moja implementácia pomocou bariery asi nie je dobrá. Avšak vysvetlenie znie, že nekonečnom cykle sa na začiatku zoradia všetky vlákna, posledné barieru odblokuje a každé sa testuje na podmienku. Vlákna nevyhovujúce podmienke sa zoraďujú opäť pri bariere, pokým vlákno, ktoré podmienke vyhovelo nedá signál na opätovné otvorenie bariery.
