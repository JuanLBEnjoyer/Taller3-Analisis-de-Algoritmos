import csv
import sys
import time
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
from taller.util.archivo_util import leer_arreglo, leer_claves, leer_claves_posicion, RAIZ
from taller.util.resultado_csv import ResultadoCsv

TAMANOS = [1_000, 10_000, 100_000, 1_000_000]
REPETICIONES = 5
MODULOS = [
    linear_search,
    binary_search,
    ternary_search,
    jump_search,
    interpolation_search,
    exponential_search,
]
RAW = RAIZ / "results" / "raw"


def medir_lote_claves(modulo, arr, claves):
    tiempos_rep = []
    num_claves = len(claves)
    for _ in range(REPETICIONES):
        ini = time.perf_counter_ns()
        for x in claves:
            modulo.buscar(arr, x)
        dur = time.perf_counter_ns() - ini
        # Guardar tiempo promedio por búsqueda en nanosegundos
        tiempos_rep.append(int(dur / num_claves))
    return tiempos_rep


def medir_clave_repetida(modulo, arr, clave, repeticiones_internas=1000):
    tiempos_rep = []
    for _ in range(REPETICIONES):
        ini = time.perf_counter_ns()
        for _ in range(repeticiones_internas):
            modulo.buscar(arr, clave)
        dur = time.perf_counter_ns() - ini
        tiempos_rep.append(int(dur / repeticiones_internas))
    return tiempos_rep


def main():
    max_n = int(sys.argv[1]) if len(sys.argv) > 1 else max(TAMANOS)
    resultados = ResultadoCsv(RAW / "busqueda_python.csv", "Python")

    print("=== EXPERIMENTO 1: Crecimiento con 1.000 claves (500 presentes, 500 ausentes) ===")
    for n in [t for t in TAMANOS if t <= max_n]:
        arr = leer_arreglo("ascendente", n)
        claves = leer_claves(n)

        for m in MODULOS:
            tiempos = medir_lote_claves(m, arr, claves)
            resultados.escribir_medido(m.NOMBRE, "ascendente", n, "general_1000", tiempos)
            prom_ns = sum(tiempos) / len(tiempos)
            print(f"{m.NOMBRE:<20} n={n:<8} {prom_ns:10.1f} ns/búsqueda ({prom_ns/1000:.3f} µs)")

    print("\n=== EXPERIMENTO 2: Posición de clave (inicio, centro, final) para n = 1.000.000 ===")
    if 1_000_000 <= max_n:
        arr_1m = leer_arreglo("ascendente", 1_000_000)
        claves_pos = leer_claves_posicion(1_000_000)
        posiciones = [("inicio", claves_pos[0]), ("centro", claves_pos[1]), ("final", claves_pos[2])]

        for nombre_pos, clave in posiciones:
            for m in MODULOS:
                tiempos = medir_clave_repetida(m, arr_1m, clave, repeticiones_internas=1000)
                resultados.escribir_medido(m.NOMBRE, "ascendente", 1_000_000, nombre_pos, tiempos)
                prom_ns = sum(tiempos) / len(tiempos)
                print(f"{m.NOMBRE:<20} pos={nombre_pos:<7} {prom_ns:10.1f} ns/búsqueda ({prom_ns/1000:.3f} µs)")

    print("\nListo benchmark de búsqueda Python.")


if __name__ == "__main__":
    main()
