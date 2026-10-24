import csv
import statistics
from pathlib import Path

REPETICIONES = 5
ENCABEZADO = ["algoritmo", "lenguaje", "variante", "n", "posicion_clave",
              "rep1", "rep2", "rep3", "rep4", "rep5",
              "promedio_ns", "desv_std_ns", "tipo"]


class ResultadoCsv:
    def __init__(self, archivo, lenguaje):
        self.archivo = Path(archivo)
        self.lenguaje = lenguaje
        self.archivo.parent.mkdir(parents=True, exist_ok=True)
        if not self.archivo.exists():
            self._agregar(ENCABEZADO, modo="w")

    def escribir_medido(self, algoritmo, variante, n, posicion_clave, tiempos_ns):
        if len(tiempos_ns) != REPETICIONES:
            raise ValueError(f"Se esperaban {REPETICIONES} repeticiones")
        promedio = statistics.mean(tiempos_ns)
        desv = statistics.stdev(tiempos_ns)      # muestral (n-1)
        self._agregar([algoritmo, self.lenguaje, variante, n, posicion_clave,
                       *tiempos_ns, f"{promedio:.1f}", f"{desv:.1f}", "medido"])

    def escribir_estimado(self, algoritmo, variante, n, posicion_clave, promedio_ns):
        self._agregar([algoritmo, self.lenguaje, variante, n, posicion_clave,
                       "", "", "", "", "", f"{promedio_ns:.1f}", "", "estimado"])

    def _agregar(self, fila, modo="a"):
        with open(self.archivo, modo, newline="") as f:
            csv.writer(f, lineterminator="\n").writerow(fila)