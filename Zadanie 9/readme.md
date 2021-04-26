## Zadanie 9

Vytvoril som program, ktorý spája 2 obrázky do jednoho. Inými slovami povedané sčítava dve trojrozmerné matice do jednej a výsledok interpretuje znovu ako obrázok.

```python
@cuda.jit
def sumImages(im1, im2, out):
    x, y, z = cuda.grid(3)

    if x < im1.shape[0] and y < im1.shape[1] and z < im1.shape[2]:
        out[x][y][z] += (im2[x][y][z] + im1[x][y][z]) % 256
```

Klasické riešenie by používalo 3 vnorené for cykly. Pri riešení pomocou technológie CUDA, sa toto dá obísť a spracovanie trvá mnohonásobne kratšie.