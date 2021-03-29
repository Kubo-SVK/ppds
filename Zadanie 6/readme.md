# Zadanie 6
## Prechod cez rieku

Pseudo kód pre entitu:
```python
def entity()
    while True:
            isCaptain = False

            # uzamkneme KO
            mutex.lock()
            counter += 1

            # ak je dost pasazierov signalizuje sa nalodenie
            if counter == 4:
                counter -= 4
                semaphore1.signal(4)
                isCaptain = True

            # signalizuje nalodenie ak existuje kombinacia moznych pasazierov
            elif counter == 2 and other_counter >= 2:
                counter -= 2
                other_counter -= 2
                semaphore1.signal(2)
                semaphore2.signal(2)
                isCaptain = True

            else:
                mutex.unlock()

            # caka sa na signal pre nalodenie
            semaphore1.wait()
            print(f'{id} nastupuje na lod')
            # samotna plavba
            sail()
```

```python
def sail():
    # caka kym vsetci nastupia
    barrier.wait()

    # cpt = kapitan
    if cpt:
        # plavba nieco trva
        sleep(randint(2, 10)/10)
        # odomknutim locku sa zacnu radit dalsie vlakna pripravene na plavbu
        mutex.unlock()
```

Synchronizácia:


Ako synchronizačné objekty som využil Mutex a Semaphore.
Mutex v tomto prípade slúži na synchronizáciu a zaručenie integrity dát.

Prvé vlákno zamkne mutex a drží ho zamknutý až pokym neskontroluje podmienky, k spusteniu plavby. Ak nie sú splnené, odomkne mutex a zaradí sa za barieru. Vlákno, ktoré zistí, že jedna z podmienok je naplnená mutex neodomyká, len signalizuje čakajúcim, že môžu pokračovať. Vo funkcii sail() je ešte bariera, ktorá zabezpečí, že všetky vlákna čo pokračovali sa dostali do tejto funkcie. Posledné vlákno, čo sa sem dostalo má rolu kapitána a po ukončení platby odomkne Mutex. To umožní radenie pre ďaľšie vlákna.

Počas vykonávania funkcie sail() vlákna môžu čakať na 2 miestach a to buď na začiatku pred zámkom mutex alebo pred volaním funkcie sail() (v kóde riadok 63 a 90). Avšak v tomto bode pred funkciou sail bude vždy maximálne 1 vlákno (dokopy aj pre officers aj pre dealers).