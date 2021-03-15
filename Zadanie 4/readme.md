# Zadanie 4
## Atomka_2.py
Druhá úloha, v ktorej sme mali vhodne upraviť implmentáciu vzorového pseudo kódu, aby spĺňala dané požiadavky.

### Analýza:
Ako prvé je potrebné implementovať barieru, ktorá zastaví monitory pred čítaním dát kým každé z čidiel nezapísalo nemeranú hednotu. Potom už nasleduje nekonečný cyklus, v ktorom sa na začiatku monitory zhromaždia na bariere. Posledný ju otvára a postupne sa dostávajú ku KO, pred ktorou uzamknú turniket, aby počas čítania dát neprišlo k ich zmene čidlom. Následne sa zoraďujú na konci cyklu, aby sa zabezpečilo, že každý monitor prečítal dáta a začínajú od znova. Čidlá v tomto príklade majú voľnú ruku a zapisujú vždy keď sa dostanú na radu a v KO sa práve nenachádza monitor.

### Pseudokód
```python
# inicializacia, kde x je pocet monitorov
def init(x):
    accessData = Semaphore(1)
    turniket = Semaphore(1)
    ls_monitor = Lightswitch()
    ls_cidlo = Lightswitch()
    validData = Event()
    barrier_1 = Barrier(x)
    barrier_2 = Barrier(x)

    for monitor_id in (0,x):
        start_thread(monitor, monitor_id)

    for cidlo_id in (0,2):
        # Cidla P a T
        start_thread(cidlo, cidlo_id)

    # Cidlo H
    start_thread(cidlo, 2)


def monitor(monitor_id):
    # cakanie, kym vsetky cidla zapisu data
    validData.wait()

    while True:
        # monitory sa zoradia na zaciatku
        bar1.wait()
        # simulacia oneskoreni medzi updatmi
        sleep(0.5)

        # zavrie sa turniket, aby sa do KO
        # nedostalo ziadne cidlo
        turniket.wait()
        # simulacia citania
        sleep(randint(40, 50) / 1000)
        # pristup k ulozisku
        pocet_citajucich_monitorov = ls_monitor.lock(accessData)
        turniket.signal()
        print(f'monit "{monitor_id:02d}": '
              f'pocet_citajucich_monitorov={pocet_citajucich_monitorov:02d}')
        # odomknutie uloziska pre ostatnych
        ls_monitor.unlock(accessData)
        # cakanie, kym sa aktualizuje kazdy monitor
        bar2.wait()


def cidlo(cidlo_id):
    while True:
        # simulacia oneskorenia aktualizacie
        sleep(randint(50, 60) / 1000)

        # kontrola, ci v KO nie je monitor
        turniket.wait()
        turniket.signal()

        # ziskanie prstupu k ulozisku
        pocet_zapisujucich_cidiel = ls_cidlo.lock(accessData)
        trvanie_zapisu = randint(wr[0], wr[1])/1000
        print(f'cidlo "{cidlo_id:02d}": '
              f'pocet_zapisujucich_cidiel={pocet_zapisujucich_cidiel:02d}, '
              f'trvanie_zapisu={trvanie_zapisu:0.3f}')
        # simulacia zapisu
        sleep(trvanie_zapisu)
        # uvolnenie uloziska
        ls_cidlo.unlock(accessData)

        # signalizacia, ze kazde cidlo 
        # uz zapisalo nejake data
        # vyuzije sa len pri prvotnom
        # spustani monitorov
        if(pocet_zapisujucich_cidiel == 2):
            validData.signal()
```

_Pozn. Ja by som to lockovanie úložiska preskočil, keďže každé čidlo má vyhradenú pamäť a monitory dáta len čítajú neupravujú. V tom prípade by si kód vyžiadol jemnú modifikáciu, keďže pri štarte spoliehame na to, že poec_zapisujucich_monitorov bude 2, čo znamená, že všetky 3 čísla. Avšak funkcionalitu, programu by to ovplyvniť nemalo. Môže jeho beh len zrýchliť, keďže vlákna by bežali plne konkurentne a čakali by len v prípade, že by v KO bol monitor._