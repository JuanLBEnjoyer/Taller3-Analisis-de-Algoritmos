from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
DIR_DATOS = RAIZ / "data"


def _leer(ruta):
    with open(ruta) as f:
        return [int(linea) for linea in f if linea.strip()]


def leer_arreglo(variante, n):
    return _leer(DIR_DATOS / f"{variante}_{n}.txt")


def leer_claves(n):
    return _leer(DIR_DATOS / f"claves_busqueda_{n}.txt")


def leer_claves_posicion(n):
    return _leer(DIR_DATOS / f"claves_posicion_{n}.txt")