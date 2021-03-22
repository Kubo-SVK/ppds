# Zadanie 5

## Modifikácia problému divochov #2
Modifikácie, úlohy 1. Existuje viac kuchárov, ktorý si navzájom pomáhajú avšak divochov k hrncu volá len jeden.

Na riešenie tohto, problému som použil len 2x synchronizačný objekt zámku Mutex, ktorý chráni v KO počítadlo.

```python
def put_servings_in_pot(): 
    while True:
        shared.cooking.lock()
        # kuchar si skontroluje, ci treba pomoct
        if(shared.active_cooks == M):
            shared.cooking.unlock()
            # ak netreba pomoct moze z kuchyne odist
            return
        # ak treba pomoct, kuchar sa zapise na prezencku
        shared.active_cooks += 1
        shared.cooking.unlock()
        print(f'kuchar {id}: varim')
        # navarenie jedla tiez cosi trva...
        sleep(0.4 + randint(0, 2) / 10)
        # kuchar do hrnca prihodi svoju cast
        shared.servings += 1
 
 
def cook():
    while True:
        # kuchari oddychuju a cakaju na svoju prilezitost
        shared.empty_pot.wait()
        # vsetci kuchari vojdu do kuchyne
        put_servings_in_pot(id, M, shared)
        shared.refill.lock()
        # ked z kuchyne kuchar vyjde da info o tom ze skoncil
        print(f'kuchar {id}: hotovo')
        # prida sa na zoznam kucharov co uz kuchynu opustili
        shared.cooks_done += 1
        # ak odchadza posledny kuchar okrem toho ze zhasne, pripravi kuchynu na dalsie pouzitie a oznami divochom, ze hrniec je plny
        if(shared.cooks_done == C):
            shared.active_cooks = 0
            shared.cooks_done = 0
            shared.full_pot.signal()
        shared.refill.unlock()
```

Moja úprava riešenia je založená na counteroch, ktoré inkrementujú kuchári: 

a) Keď idú pomôcť s varením

b) Keď z kuchyne odchádzajú

V kuchyni každý kuchár varí jednu časť. Pri vchode sa vedie "prezenčka" (counter active_cooks), ktorá umožní priložiť ruku k dielu, len toľkým kuchárom, koľkých na prípravu jedla treba. Ak kuchár skončí je jeho povinnosť sa ísť pozrieť, či sa s niečim ešte nedá pomôcť. V prípade, že nie môže opustiť kuchyňu a ísť oddychovať. Pri odchode sa každý kuchár musí zapísať (counter cooks_done), že kuchynňu opustil. Posledný kuchár okrem toho, že v kuchyni zhasne ju musí aj pripraviť na ďaľší deň a teda vynuluje prezenčky. Ako poslednú vec pred zaslúženým oddychom zvolá divochov k hrncu. Po vyprázdnený hrnca jeden z divochov zvoláva všetk=ych kuchárov do kuchyne a cyklus sa opakuje.

_Bez príbehu:_

1) Pri vstupe do funkcii *put_servings_in_pot()* sa inkrementuje counter active_cooks, ak sa tento counter rovná počtu porcií (divochov), tak vlákno z funkcie vystúpi.

2) Po návrate do funkcii *cook()* je ďaľší counter. cooks_done, ten zabezpečuje, že až posledné vlákno môže signalizovať, že je navarené, ale ešte pred tým vynuluje oba countre.

Keďže oba countre musia byť zdieľané, tak v progame sú chránené pomocou zámku Mutex pre zabezpečenie integrity.