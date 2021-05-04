## Zadanie 10

Modifikoval som príklad zo zadania 9, aj keď v tomto prípade sa mi nepodarilo zachovať rovnakú funkcionalitu a obrízok sa nesčíta, ale len sa zmenia jeho farby.

Pri modifikácii dáta serializujem, posielam v rúdoch do GPU a výsledné dáta opäť prevádzam na 3 rozmerné pole.

Táto implementácia však stačila na meranie výkonu pri použítí rôznej dĺžky vstupných dát.

| #    | Mean kernel duration | Standard deviation | Total time | kernel duration / deviation |
|------|----------------------|--------------------|------------|-----------------------------|
| 1    | 13,367 ms            | 0 ms               | 0,484 s    | 0,00 %                      |
| 2    | 6,378 ms             | 0,134 ms           | 0,295 s    | 2,10 %                      |
| 4    | 3,515 ms             | 0,222 ms           | 0,273 s    | 6,32 %                      |
| 8    | 2,285 ms             | 0,364 ms           | 0,298 s    | 15,93 %                     |
| 16   | 1,938 ms             | 0,594 ms           | 0,307 s    | 30,65 %                     |
| 32   | 2,525 ms             | 0,546 ms           | 0,502 s    | 21,62 %                     |
| 64   | 6,382 ms             | 1,212 ms           | 0,301 s    | 18,99 %                     |
| 128  | 9,812 ms             | 1,282 ms           | 0,281 s    | 13,07 %                     |
| 256  | 15,842 ms            | 2,757 ms           | 0,277 s    | 17,40 %                     |
| 512  | 33,179 ms            | 4,774 ms           | 0,273 s    | 14,39 %                     |
| 1024 | 76,832 ms            | 7,666 ms           | 0,337 s    | 9,98 %                      |
| 2048 | 153,493 ms           | 18,974 ms          | 0,399 s    | 12,36 %                     |
| 4096 | 286,383 ms           | 31,737 ms          | 0,526 s    | 11,08 %                     |
| 8192 | 569,894 ms           | 63,861 ms          | 0,702 s    | 11,21 %                     |



V tabuľke, prvý stĺpec označuje, na koľko častí bolo rozdelené vstupné pole o veľkosti 1 048 576 (512\*512\*4). Z meraní sa dá vidieť, že pri rozdelení poľa na príliš veľa menších začína celkový čas výpočtu rýchlo stúpať. Tento trend by pokračoval aj nadaľej. Tiež si môžme všimnúť, že priemerný čas strávený pri výpočte na GPU ku koncu rýchlo vzrástol, keďže bolo už potrebné vykonať veľa posunov v pamäti. 

Žiaľ sa mi nepodarilo použiť profiler. Pre pužitie bolo potrebné doinštalovat nvtx-plugins package do Pythonu, avšak autori nepodporujú windows a priamo pribalený profiler Nvidia si s python programom nevedel poradiť a písal ERROR. Z tohto dôvodu, som zostal, len pri meraniach a manuálnom skúšaní rôznych dĺžok poľa. Zatiaľ, čo pri prvych testoch bolo spracovanie dát k výpočtu výrazne pomalašie, zhoršenou optimalizáciou sa výpočet na GPU stal neefektívny a spracovanie dát už nebolo kameňom úrazu.

*Pozn. Testované na GPU Nvidia GTX 970 