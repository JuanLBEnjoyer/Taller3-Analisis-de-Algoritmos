import random
from pathlib import Path

SEMILLA = 42
TAMANOS = [1_000, 10_000, 100_000, 1_000_000]
VALOR_MIN = 10_000_000          
VALOR_MAX = 99_999_999         
CLAVES_PRESENTES = 500
CLAVES_AUSENTES = 500

DIR_DATOS = Path(__file__).resolve().parent.parent / "data"


def escribir(nombre, valores):
    with open(DIR_DATOS / nombre, "w") as f:
        f.write("\n".join(map(str, valores)))
        f.write("\n")


def generar_claves(rng, arreglo):
    presentes = rng.sample(arreglo, CLAVES_PRESENTES)

    existentes = set(arreglo)      
    ausentes, vistos = [], set()
    while len(ausentes) < CLAVES_AUSENTES:
        c = rng.randint(VALOR_MIN, VALOR_MAX)
        if c not in existentes and c not in vistos:
            vistos.add(c)
            ausentes.append(c)

    claves = presentes + ausentes
    rng.shuffle(claves)
    return claves


def main():
    DIR_DATOS.mkdir(exist_ok=True)
    rng = random.Random(SEMILLA)

    for n in TAMANOS:
        aleatorio = [rng.randint(VALOR_MIN, VALOR_MAX) for _ in range(n)]
        ascendente = sorted(aleatorio)
        descendente = ascendente[::-1]

        escribir(f"aleatorio_{n}.txt", aleatorio)
        escribir(f"ascendente_{n}.txt", ascendente)
        escribir(f"descendente_{n}.txt", descendente)

        escribir(f"claves_busqueda_{n}.txt", generar_claves(rng, aleatorio))
        escribir(f"claves_posicion_{n}.txt",
                 [ascendente[0], ascendente[n // 2], ascendente[-1]])

        assert min(aleatorio) >= VALOR_MIN and max(aleatorio) <= VALOR_MAX
        print(f"n = {n:>9,}: archivos generados")


if __name__ == "__main__":
    main()