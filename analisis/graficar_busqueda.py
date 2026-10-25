import csv
import matplotlib.pyplot as plt
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DIR_RAW = RAIZ / "results" / "raw"
DIR_GRAFICAS = RAIZ / "results" / "graficas"

COLORES = {
    "LinearSearch": "#e74c3c",         # Rojo
    "JumpSearch": "#e67e22",           # Naranja
    "BinarySearch": "#2980b9",         # Azul
    "TernarySearch": "#8e44ad",        # Morado
    "ExponentialSearch": "#27ae60",    # Verde
    "InterpolationSearch": "#16a085",  # Turquesa
}

MARCADORES = {
    "LinearSearch": "o",
    "JumpSearch": "s",
    "BinarySearch": "^",
    "TernarySearch": "v",
    "ExponentialSearch": "D",
    "InterpolationSearch": "p",
}


def cargar_registros():
    registros = []
    for archivo, lenguaje in [("busqueda_python.csv", "Python"), ("busqueda_java.csv", "Java")]:
        ruta = DIR_RAW / archivo
        if not ruta.exists():
            continue
        with open(ruta, newline="") as f:
            lector = csv.DictReader(f)
            for fila in lector:
                fila["n"] = int(fila["n"])
                fila["promedio_ns"] = float(fila["promedio_ns"])
                registros.append(fila)
    return registros


def graficar_crecimiento_lenguaje(registros, lenguaje):
    sub = [r for r in registros if r["lenguaje"] == lenguaje and r["posicion_clave"] == "general_1000"]
    
    algoritmos = sorted(list(set(r["algoritmo"] for r in sub)))
    
    fig, ax = plt.subplots(figsize=(9, 6), dpi=300)
    
    for alg in algoritmos:
        datos_alg = sorted([r for r in sub if r["algoritmo"] == alg], key=lambda x: x["n"])
        xs = [r["n"] for r in datos_alg]
        ys = [r["promedio_ns"] / 1000.0 for r in datos_alg]  # a microsegundos
        
        ax.plot(
            xs,
            ys,
            label=alg,
            color=COLORES.get(alg, "#333333"),
            marker=MARCADORES.get(alg, "o"),
            linewidth=2,
            markersize=7,
        )

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Tamaño del Arreglo (n)", fontsize=11, fontweight="bold")
    ax.set_ylabel("Tiempo Promedio por Búsqueda (µs)", fontsize=11, fontweight="bold")
    ax.set_title(f"Punto 2: Desempeño de Búsqueda vs n ({lenguaje})\n(1.000 Claves: 500 Presentes, 500 Ausentes)", fontsize=12, fontweight="bold")
    ax.grid(True, which="both", linestyle="--", alpha=0.5)
    ax.legend(title="Algoritmo", loc="upper left", frameon=True)
    
    plt.tight_layout()
    nombre_archivo = f"crecimiento_busqueda_{lenguaje.lower()}.png"
    ruta_guardado = DIR_GRAFICAS / nombre_archivo
    plt.savefig(ruta_guardado)
    plt.close()
    print(f"Gráfica guardada: {ruta_guardado}")


def graficar_compilado_vs_interpretado(registros):
    sub = [r for r in registros if r["n"] == 1_000_000 and r["posicion_clave"] == "general_1000"]
    
    algoritmos = [
        "LinearSearch",
        "JumpSearch",
        "BinarySearch",
        "TernarySearch",
        "ExponentialSearch",
        "InterpolationSearch",
    ]
    
    py_tiempos = []
    java_tiempos = []
    
    for alg in algoritmos:
        r_py = [r["promedio_ns"] for r in sub if r["algoritmo"] == alg and r["lenguaje"] == "Python"]
        r_java = [r["promedio_ns"] for r in sub if r["algoritmo"] == alg and r["lenguaje"] == "Java"]
        py_tiempos.append(r_py[0] / 1000.0 if r_py else 0)
        java_tiempos.append(r_java[0] / 1000.0 if r_java else 0)
        
    x = range(len(algoritmos))
    ancho = 0.38
    
    fig, ax = plt.subplots(figsize=(11, 7), dpi=300)
    
    pos_java = [i - ancho/2 for i in x]
    pos_py = [i + ancho/2 for i in x]
    
    rects1 = ax.bar(pos_java, java_tiempos, ancho, label="Java (Compilado / JIT)", color="#2b5797")
    rects2 = ax.bar(pos_py, py_tiempos, ancho, label="Python (Interpretado)", color="#f39c12")
    
    ax.set_yscale("log")
    ax.set_ylabel("Tiempo Promedio por Búsqueda (µs) [Escala Log]", fontsize=11, fontweight="bold")
    ax.set_title("Punto 2: Comparación Compilado (Java) vs Interpretado (Python)\n(n = 1.000.000 elementos, 1.000 claves)", fontsize=13, fontweight="bold")
    ax.set_xticks(list(x))
    ax.set_xticklabels(algoritmos, rotation=15, ha="right", fontsize=10, fontweight="bold")
    ax.legend(frameon=True, fontsize=11)
    ax.grid(axis="y", which="both", linestyle="--", alpha=0.5)
    
    for rect in rects1:
        altura = rect.get_height()
        texto = f"{altura:.2f} µs" if altura >= 1 else f"{altura*1000:.0f} ns"
        ax.annotate(texto,
                    xy=(rect.get_x() + rect.get_width() / 2, altura),
                    xytext=(0, 4),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8, rotation=0, fontweight="bold")
                    
    for rect in rects2:
        altura = rect.get_height()
        texto = f"{altura:.2f} µs" if altura < 1000 else f"{altura/1000:.1f} ms"
        ax.annotate(texto,
                    xy=(rect.get_x() + rect.get_width() / 2, altura),
                    xytext=(0, 4),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8, rotation=0, fontweight="bold")

    plt.tight_layout()
    ruta_guardado = DIR_GRAFICAS / "comparativa_busqueda_java_vs_python_1m.png"
    plt.savefig(ruta_guardado)
    plt.close()
    print(f"Gráfica guardada: {ruta_guardado}")


def generar_tablas_posicion_clave(registros):
    sub = [r for r in registros if r["n"] == 1_000_000 and r["posicion_clave"] in ("inicio", "centro", "final")]
    
    algoritmos = [
        "LinearSearch",
        "JumpSearch",
        "BinarySearch",
        "TernarySearch",
        "InterpolationSearch",
        "ExponentialSearch",
    ]
    
    for lenguaje in ["Java", "Python"]:
        print(f"\n### Tabla Posición de la Clave (n = 1.000.000) - {lenguaje}")
        print("| Algoritmo | Clave al Inicio | Clave al Centro | Clave al Final |")
        print("|---|---|---|---|")
        
        for alg in algoritmos:
            t_ini = [r["promedio_ns"] for r in sub if r["lenguaje"] == lenguaje and r["algoritmo"] == alg and r["posicion_clave"] == "inicio"]
            t_cen = [r["promedio_ns"] for r in sub if r["lenguaje"] == lenguaje and r["algoritmo"] == alg and r["posicion_clave"] == "centro"]
            t_fin = [r["promedio_ns"] for r in sub if r["lenguaje"] == lenguaje and r["algoritmo"] == alg and r["posicion_clave"] == "final"]
            
            ini_val = t_ini[0] if t_ini else 0
            cen_val = t_cen[0] if t_cen else 0
            fin_val = t_fin[0] if t_fin else 0
            
            def fmt(ns):
                if ns >= 1_000_000:
                    return f"{ns / 1e6:.2f} ms ({ns:,.0f} ns)"
                elif ns >= 1_000:
                    return f"{ns / 1e3:.2f} µs ({ns:,.0f} ns)"
                else:
                    return f"{ns:.1f} ns"

            print(f"| {alg} | {fmt(ini_val)} | {fmt(cen_val)} | {fmt(fin_val)} |")


def main():
    DIR_GRAFICAS.mkdir(parents=True, exist_ok=True)
    registros = cargar_registros()
    
    graficar_crecimiento_lenguaje(registros, "Java")
    graficar_crecimiento_lenguaje(registros, "Python")
    graficar_compilado_vs_interpretado(registros)
    generar_tablas_posicion_clave(registros)


if __name__ == "__main__":
    main()
