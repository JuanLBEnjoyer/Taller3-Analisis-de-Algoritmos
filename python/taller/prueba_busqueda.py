import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from taller.search import (
    linear_search,
    binary_search,
    ternary_search,
    jump_search,
    interpolation_search,
    exponential_search,
)

modulos = [
    linear_search,
    binary_search,
    ternary_search,
    jump_search,
    interpolation_search,
    exponential_search,
]

rnd = random.Random(42)

for m in modulos:
    ok = True
    for n in [0, 1, 2, 5, 20, 100, 1000]:
        if n == 0:
            arr = []
        else:
            arr = sorted([rnd.randint(10_000_000, 99_999_999) for _ in range(n)])

        # Probar elementos presentes
        for _ in range(min(n, 10)):
            idx = rnd.randrange(n)
            val = arr[idx]
            res = m.buscar(arr, val)
            if res < 0 or res >= n or arr[res] != val:
                ok = False
                print(f"FALLO presente: {m.NOMBRE} n={n} val={val} res={res}")
                break

        # Probar elementos ausentes
        for _ in range(10):
            val = rnd.randint(10_000_000, 99_999_999)
            if val not in arr:
                res = m.buscar(arr, val)
                if res != -1:
                    ok = False
                    print(f"FALLO ausente: {m.NOMBRE} n={n} val={val} res={res}")
                    break

        # Probar extremos
        if n > 0:
            for val in [arr[0], arr[n // 2], arr[-1]]:
                res = m.buscar(arr, val)
                if res == -1 or arr[res] != val:
                    ok = False
                    print(f"FALLO extremo: {m.NOMBRE} n={n} val={val} res={res}")
                    break

    print(f"{m.NOMBRE}: {'OK' if ok else 'CON ERRORES'}")
