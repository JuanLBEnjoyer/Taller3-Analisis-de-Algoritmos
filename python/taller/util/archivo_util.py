from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
DIR_DATOS = RAIZ / "data"


def _leer(ruta):
    with open(ruta) as f:
        return [int(linea) for linea in f if linea.strip()]


def _resolver_ruta(n, nombre_archivo):
    ruta_sub = DIR_DATOS / str(n) / nombre_archivo
    if ruta_sub.exists():
        return ruta_sub
    return DIR_DATOS / nombre_archivo


def leer_arreglo(variante, n):
    return _leer(_resolver_ruta(n, f"{variante}_{n}.txt"))


def leer_claves(n):
    return _leer(_resolver_ruta(n, f"claves_busqueda_{n}.txt"))


def leer_claves_posicion(n):
    return _leer(_resolver_ruta(n, f"claves_posicion_{n}.txt"))