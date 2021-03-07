## Čitatelia-Zapisovatelia

Implementoval som úlohu čitatelia-Zapisovatelia, bez vyhľadovenia. Na implementáciu som použil LightSwitch, z orvej úlohy. Program som nastavil tak, aby bežal vždy 10s keďže za tú dobu by sa stihli vystriedať všetky vlákna niekoľko krát.

```python
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
```

Takto som implementoval funkcie pre čitateľa a zapisovateľa. Každý beží v nekonečnom loope, ktorý sa ukonči až po vypršaní časového limitu. pred vstupom do kritickej oblasti je ešte jedno vynútené prepnutie, aby sa do testu vložil prvok náhodnosti, ktoré vlákna sa budú spúštať. 

Čitatelia prepínajú LightSwitch ako bolo ukázané na prednáške, zatiaľ čo zapisovatelia prepínajú semafór (zámok miestnosti).

---
## Odpovede na otázky:
5) Problém vyhľadovenia sa u mňa prejavoval, keď bolo čitateľov násobne viac ako zapisovateľov. V tomto prípade sa zapisovatelia dostávali na rad, až po ukončení vlákien zapisovateľov.

7. Áno napríklad v prípade, že by sa zmenil pomer a zapisovateľov, by bolo násovne viac ako čitateľov.

9) Keď vychádzam z mojich testov, tak pri implmentácii bez vyhľadovenia to závisí od HW na ktorom kód beží a teda ako plánovač prepína medzi vláknami.