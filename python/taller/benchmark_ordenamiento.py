import csv
import math
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from taller.sorting import (insertion_sort, dual_pivot_quicksort, merge_sort,
                            heap_sort, radix_sort, bucket_sort)
from taller.util.archivo_util import leer_arreglo, RAIZ
from taller.util.resultado_csv import ResultadoCsv
from taller.util.verificador import verificar

TAMANOS = [1_000, 10_000, 100_000, 1_000_000]
VARIANTES = ["aleatorio", "ascendente", "descendente"]
REPETICIONES = 5
LIMITE_NS = 300 * 1_000_000_000
RAW = RAIZ / "results" / "raw"
INCIDENTES = RAW / "incidentes_ordenamiento_python.csv"
MODULOS = [insertion_sort, dual_pivot_quicksort, merge_sort,
           heap_sort, radix_sort, bucket_sort]


def prediccion(modulo, n_prev, prom_prev, n):
    """Tiempo previsto para n, extrapolando desde el tamaño anterior medido."""
    r = n / n_prev
    if modulo is insertion_sort:
        factor = r * r                                  
    else:
        factor = r * math.log(n) / math.log(n_prev)    
    return prom_prev * factor


def incidente(modulo, variante, n, motivo):
    fila = [modulo.NOMBRE, "Python", variante, n, motivo]
    with open(INCIDENTES, "a", newline="") as f:
        csv.writer(f, lineterminator="\n").writerow(fila)
    print("  INCIDENTE:", ",".join(map(str, fila)))


def medir(modulo, original):
    """Devuelve (tiempos, None) si todo salió bien, o (None, motivo)."""
    tiempos = []
    try:
        for _ in range(REPETICIONES):
            copia = original[:]                          
            ini = time.perf_counter_ns()
            modulo.ordenar(copia)
            dur = time.perf_counter_ns() - ini

            if not verificar(original, copia):
                raise RuntimeError(f"Resultado incorrecto: {modulo.NOMBRE}")
            tiempos.append(dur)
            if dur > LIMITE_NS:
                return None, f"excede_5_min({dur}ns)"
    except RecursionError:
        return None, "RecursionError"
    return tiempos, None


def main():
    max_n = int(sys.argv[1]) if len(sys.argv) > 1 else max(TAMANOS)

    resultados = ResultadoCsv(RAW / "ordenamiento_python.csv", "Python")
    if not INCIDENTES.exists():
        INCIDENTES.write_text("algoritmo,lenguaje,variante,n,motivo\n")

    previo = {}        
    bloqueados = set()

    for variante in VARIANTES:
        for n in [t for t in TAMANOS if t <= max_n]:
            original = leer_arreglo(variante, n)     

            for m in MODULOS:
                clave = (m.NOMBRE, variante)

                if clave in bloqueados:
                    incidente(m, variante, n, "omitido_por_n_menor")
                    continue
                if clave in previo and prediccion(m, *previo[clave], n) > LIMITE_NS:
                    bloqueados.add(clave)
                    incidente(m, variante, n, "timeout_previsto")
                    continue

                tiempos, motivo = medir(m, original)
                if motivo:
                    bloqueados.add(clave)
                    incidente(m, variante, n, motivo)
                else:
                    resultados.escribir_medido(m.NOMBRE, variante, n, "NA", tiempos)
                    prom = sum(tiempos) / len(tiempos)
                    previo[clave] = (n, prom)
                    print(f"{m.NOMBRE:<20} {variante:<11} n={n:<8} {prom / 1e6:12.3f} ms")
    print("Listo.")


if __name__ == "__main__":
    main()