import random
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from taller.sorting import (insertion_sort, dual_pivot_quicksort, merge_sort,
                            heap_sort, radix_sort, bucket_sort)
from taller.util.verificador import verificar

modulos = [insertion_sort, dual_pivot_quicksort, merge_sort,
           heap_sort, radix_sort, bucket_sort]
rnd = random.Random(1)

for m in modulos:
    ok = True
    for n in [0, 1, 2, 5, 50, 300]:
        for caso in range(4):
            if caso == 3:
                original = [10_000_000 + rnd.randint(0, 4) for _ in range(n)]
            else:
                original = [rnd.randint(10_000_000, 99_999_999) for _ in range(n)]
            if caso == 1:
                original.sort()
            if caso == 2:
                original.sort(reverse=True)
            copia = original[:]
            m.ordenar(copia)
            if not verificar(original, copia):
                ok = False
                print(f"FALLO: {m.NOMBRE} n={n} caso={caso}")
    print(f"{m.NOMBRE}: {'OK' if ok else 'CON ERRORES'}")