## Zadanie 8

Program má v "crypto.txt" zoznam cryptocoinov, pre ktoré z API ťahá dáta o ich hodnote v eurách. Pre viditeľný rozdiel, som do súboru vložil 100 symbolov. Program sa posiela GET requesty na verejné API, ktoré nepotrebuje žiadnu autentifikáciu API kľúčom avšak stále je obmedzená.

Merania:

| #   | Async | Sync  |
|-----|-------|-------|
| 5   | 0,95  | 1,59  |
| 10  | 0,75  | 2,77  |
| 15  | 1,74  | 8,02  |
| 20  | 1,26  | 5,61  |
| 25  | 1,51  | 6,48  |
| 30  | 2,55  | 8,72  |
| 35  | 4,66  | 10,54 |
| 40  | 2,11  | 11,91 |
| 45  | 2,27  | 12,76 |
| 50  | 4,43  | 13,97 |
| 55  | 4,03  | 15,83 |
| 60  | 3,02  | 16,35 |
| 65  | 4,35  | 18,74 |
| 70  | 8,01  | 19,67 |
| 75  | 4,1   | 23,87 |
| 80  | 4     | 25,46 |
| 85  | 4,19  | 28,15 |
| 90  | 4,68  | 27,5  |
| 95  | 4,36  | 31,5  |
| 100 | 4,28  | 33,88 |

*\# - počet requestov

Graf z tejto tabuľky aj táto tabuľka sa nachádza v priečinku Meranie.

V dátach, sú relatívne nepresnosti spôsobené samotnou API, avšak vyskytujú sa zriedkavo, takže z merania vidno rozdiel medzi synchrónnymi a asynchronnymi volaniami, kde execution time synchrónnych volaní má tendenciu rásť lineárne. Pri asynchrónnych je skoro konštantný aj pri veľkom množstve requestov.