# Zadanie 1

Implementujte dve vlákna, ktoré budú používať spoločný index do spoločného poľa (inicializovaného na hodnoty 0) istej veľkosti. Každé vlákno nech inkrementuje ten prvok poľa, kam práve ukazuje spoločný index. Následne nech index zvýši. Ak už index ukazuje mimo poľa, vlákno svoju činnosť skončí. Po skončení vlákien spočítajte, koľko prvkov poľa má hodnotu 1. Ak zistíte, že nie každý prvok poľa má hodnotu 1, modifikujte program tak, aby na koniec (po skončení behu vlákien) zistil početnosti (histogram) hodnôt, ktoré sa nachádzajú v poli.

---
## vlakna_1.py

```python
def computation(obj):
    obj.mutex.lock()  #locknutie
    while True:
        if obj.counter >= obj.end:
            break
        
        obj.elms[obj.counter] += 1
        obj.counter += 1
    obj.mutex.unlock() #unlocknutie
```

Táto implementácia síce poskytne očakávaný výsledok, ale všetky výpočty sa odohrajú len v 1. vlákne a 2. vlákno sa dostane na rad až keď prvé skončí (counter = 1 000 000). To však znamená, že ukončovacia podmienka je splnená a skončí aj drué vlákno.

Takže táto implementácia je pre konkurentné prgramovanie úplne nevhodná.

---
## vlakna_2.py

```python
def computation(obj):
    while True:
        if obj.counter >= obj.end:
            break
        
        obj.mutex.lock() #locknutie
        obj.elms[obj.counter] += 1
        obj.counter += 1
        obj.mutex.unlock() #unlocknutie
```

Takto umiestnené lockovanie zabraňuje viac násobnej inkrementácii tej istej hodnoty v poli a aj preskočeniu niektorých prvkov. Avšak stále môže nastať situácia, kde budeme inkrementovať prvok mimo rozsah poľa. To nastane, keď jedno vlákno inkrementuje, counter na konečnú hodnotu a uvoľní svoj zámok. Po uvolnení zámku prvého vlákna sa začne vykonávať vlákno druhé. Avšak toto vlákno čakalo už za ukončovacou podmienkou, takže pracuje s hodnotou counter == 1 000 000, čo je mimo rozsah poľa.

---
## vlakna_3.py

```python
def computation(obj):
    while True:
        obj.mutex.lock() #locknutie
        if obj.counter >= obj.end:
            obj.mutex.unlock() #unlocknutie
            break
        
        obj.elms[obj.counter] += 1
        obj.counter += 1
        obj.mutex.unlock() #unlocknutie
```

Toto je najsprávnejšie riešenie, aké sa mi podarilo. Vlákno si lockne objekt počas celého výpočtu, vrátane kontroly ukončovacej podmienky. Nech systémový plánovač spúšta jadrá v akom koľvek poradí, vždy bude jedno čakať ešte pred overením ukončovacej podmienky. Keďže vlákna lockujú ešte pred ukončovacou podmienkou, treba po jej splnení zámok uvoľniť, aby sa predišlo dead-locku.