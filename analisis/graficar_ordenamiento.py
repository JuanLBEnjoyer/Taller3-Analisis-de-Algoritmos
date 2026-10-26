import csv
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DIR_RAW = RAIZ / "results" / "raw"
DIR_GRAFICAS = RAIZ / "results" / "graficas"

ALGORITMOS = [
    "InsertionSort",
    "DualPivotQuickSort",
    "MergeSort",
    "HeapSort",
    "RadixSort",
    "BucketSort",
]

COLORES_ALGORITMOS = {
    "InsertionSort": "#e74c3c",       # Rojo
    "DualPivotQuickSort": "#e67e22",  # Naranja
    "MergeSort": "#2980b9",           # Azul
    "HeapSort": "#8e44ad",            # Morado
    "RadixSort": "#16a085",           # Turquesa
    "BucketSort": "#27ae60",          # Verde
}

MARCADORES = {
    "InsertionSort": "o",
    "DualPivotQuickSort": "s",
    "MergeSort": "^",
    "HeapSort": "D",
    "RadixSort": "v",
    "BucketSort": "P",
}

COLORES_VARIANTES = {
    "aleatorio": "#2980b9",    # Azul
    "ascendente": "#27ae60",   # Verde
    "descendente": "#c0392b",  # Rojo oscuro
}


def cargar_registros():
    registros = []
    for archivo, lenguaje in [("ordenamiento_java.csv", "Java"), ("ordenamiento_python.csv", "Python")]:
        ruta = DIR_RAW / archivo
        if not ruta.exists():
            continue
        with open(ruta, newline="") as f:
            lector = csv.DictReader(f)
            for fila in lector:
                fila["n"] = int(fila["n"])
                fila["promedio_ns"] = float(fila["promedio_ns"])
                fila["tiempo_ms"] = fila["promedio_ns"] / 1e6
                registros.append(fila)
    return registros


def formato_tiempo(ms):
    """Devuelve una etiqueta legible del tiempo según su magnitud."""
    if ms >= 60_000:
        return f"{ms / 60_000:.1f} min"
    elif ms >= 1_000:
        return f"{ms / 1_000:.2f} s"
    elif ms >= 1:
        return f"{ms:.2f} ms"
    elif ms >= 0.001:
        return f"{ms * 1_000:.1f} µs"
    else:
        return f"{ms * 1e6:.0f} ns"


def graficar_crecimiento(registros, lenguaje):
    """Gráfica de líneas de n vs tiempo en escala log-log para entrada aleatoria."""
    sub = [r for r in registros if r["lenguaje"] == lenguaje and r["variante"] == "aleatorio"]
    if not sub:
        return

    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)

    for alg in ALGORITMOS:
        datos_alg = sorted([r for r in sub if r["algoritmo"] == alg], key=lambda x: x["n"])
        if not datos_alg:
            continue

        xs = [r["n"] for r in datos_alg]
        ys = [r["tiempo_ms"] for r in datos_alg]
        tipos = [r["tipo"] for r in datos_alg]

        color = COLORES_ALGORITMOS.get(alg, "#333333")
        marker = MARCADORES.get(alg, "o")

        # Dibujar segmentos: medidos continuos, estimados punteados
        for i in range(len(xs) - 1):
            estilo = "--" if (tipos[i] == "estimado" or tipos[i + 1] == "estimado") else "-"
            alfa = 0.85 if estilo == "-" else 0.65
            ax.plot(
                [xs[i], xs[i + 1]],
                [ys[i], ys[i + 1]],
                linestyle=estilo,
                color=color,
                linewidth=2.2,
                alpha=alfa,
            )

        # Dibujar puntos con marcador
        for x_val, y_val, t_val in zip(xs, ys, tipos):
            if t_val == "estimado":
                ax.scatter(
                    x_val,
                    y_val,
                    color="white",
                    edgecolor=color,
                    marker=marker,
                    s=80,
                    linewidth=2,
                    zorder=4,
                )
            else:
                ax.scatter(
                    x_val,
                    y_val,
                    color=color,
                    marker=marker,
                    s=60,
                    zorder=4,
                )

        # Etiqueta para la leyenda con línea continua
        ax.plot([], [], color=color, marker=marker, label=alg, linewidth=2)

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Tamaño del Arreglo (n) [Escala Log]", fontsize=11, fontweight="bold")
    ax.set_ylabel("Tiempo de Ejecución (ms) [Escala Log]", fontsize=11, fontweight="bold")
    ax.set_title(
        f"Punto 1: Curva de Crecimiento - {lenguaje}\n(Entrada Aleatoria, 5 Repeticiones, Escala Log-Log)",
        fontsize=13,
        fontweight="bold",
    )
    ax.grid(True, which="both", linestyle="--", alpha=0.45)

    # Elementos de apoyo en la leyenda
    hay_estimados = any(r["tipo"] == "estimado" for r in sub)
    if hay_estimados:
        ax.plot([], [], color="#555555", linestyle="-", label="Línea sólida: Medido")
        ax.plot([], [], color="#555555", linestyle="--", marker="o", markerfacecolor="white", label="Punteada / hueca: Estimado")

    ax.legend(loc="upper left", frameon=True, fontsize=9.5, ncol=2)

    plt.tight_layout()
    nombre_archivo = f"crecimiento_ordenamiento_{lenguaje.lower()}.png"
    ruta_guardado = DIR_GRAFICAS / nombre_archivo
    plt.savefig(ruta_guardado)
    plt.close()
    print(f"Gráfica generada: {ruta_guardado}")


def graficar_efecto_orden(registros, n_tamano):
    """Gráfico de barras para el lenguaje compilado (Java) comparando las 3 variantes."""
    sub = [r for r in registros if r["lenguaje"] == "Java" and r["n"] == n_tamano]
    if not sub:
        return

    variantes = ["aleatorio", "ascendente", "descendente"]
    x = np.arange(len(ALGORITMOS))
    ancho = 0.26

    fig, ax = plt.subplots(figsize=(12, 7), dpi=300)

    for i, var in enumerate(variantes):
        tiempos = []
        estimados = []
        for alg in ALGORITMOS:
            r = next((item for item in sub if item["algoritmo"] == alg and item["variante"] == var), None)
            if r:
                tiempos.append(r["tiempo_ms"])
                estimados.append(r["tipo"] == "estimado")
            else:
                tiempos.append(0.0)
                estimados.append(False)

        pos = x + (i - 1) * ancho
        color = COLORES_VARIANTES[var]

        for p, t, est in zip(pos, tiempos, estimados):
            hatch = "//" if est else ""
            alpha = 0.7 if est else 0.95
            rect = ax.bar(
                p,
                t,
                ancho,
                color=color,
                edgecolor="#1a1a1a" if est else color,
                hatch=hatch,
                alpha=alpha,
                linewidth=1.2 if est else 0.5,
            )
            # Anotación sobre la barra
            if t > 0:
                texto = formato_tiempo(t)
                if est:
                    texto += "*"
                ax.annotate(
                    texto,
                    xy=(p, t),
                    xytext=(0, 4),
                    textcoords="offset points",
                    ha="center",
                    va="bottom",
                    fontsize=7.5,
                    rotation=30,
                    fontweight="bold" if not est else "normal",
                )

        # Barra dibujada correctamente
        pass

    handles = [
        mpatches.Patch(
            facecolor=COLORES_VARIANTES["aleatorio"],
            edgecolor="#1a1a1a",
            linewidth=0.6,
            label="Variante: Aleatorio",
        ),
        mpatches.Patch(
            facecolor=COLORES_VARIANTES["ascendente"],
            edgecolor="#1a1a1a",
            linewidth=0.6,
            label="Variante: Ascendente",
        ),
        mpatches.Patch(
            facecolor=COLORES_VARIANTES["descendente"],
            edgecolor="#1a1a1a",
            linewidth=0.6,
            label="Variante: Descendente",
        ),
    ]
    if any(r["tipo"] == "estimado" for r in sub):
        handles.append(
            mpatches.Patch(
                facecolor="#f2f2f2",
                edgecolor="#333333",
                hatch="//",
                linewidth=0.8,
                label="* Rayado: Estimado",
            )
        )

    ax.set_yscale("log")
    ax.set_ylabel("Tiempo Promedio (ms) [Escala Log]", fontsize=11, fontweight="bold")
    ax.set_title(
        f"Punto 1: Efecto del Orden de Entrada en Java (n = {n_tamano:,} elementos)\n(Aleatorio vs Ascendente vs Descendente)",
        fontsize=13,
        fontweight="bold",
    )
    ax.set_xticks(x)
    ax.set_xticklabels(ALGORITMOS, rotation=15, ha="right", fontsize=10, fontweight="bold")
    ax.grid(axis="y", which="both", linestyle="--", alpha=0.45)
    ax.legend(
        handles=handles,
        loc="upper right",
        frameon=True,
        framealpha=0.92,
        edgecolor="#cccccc",
        fontsize=9.5,
    )

    # Margen superior e inferior para evitar solapamiento con la leyenda o corte de etiquetas
    y_max = max([r["tiempo_ms"] for r in sub]) * 18.0
    y_min = min([r["tiempo_ms"] for r in sub if r["tiempo_ms"] > 0]) * 0.3
    ax.set_ylim(y_min, y_max)

    plt.tight_layout()
    nombre_archivo = f"efecto_orden_java_{n_tamano}.png"
    ruta_guardado = DIR_GRAFICAS / nombre_archivo
    plt.savefig(ruta_guardado)
    plt.close()
    print(f"Gráfica generada: {ruta_guardado}")


def graficar_compilado_vs_interpretado(registros):
    """Gráfico de barras para n = 1.000.000 con entrada aleatoria comparando Java vs Python."""
    sub = [r for r in registros if r["n"] == 1_000_000 and r["variante"] == "aleatorio"]
    if not sub:
        return

    x = np.arange(len(ALGORITMOS))
    ancho = 0.36

    fig, ax = plt.subplots(figsize=(11, 7), dpi=300)

    java_tiempos, java_est = [], []
    py_tiempos, py_est = [], []

    for alg in ALGORITMOS:
        r_j = next((r for r in sub if r["algoritmo"] == alg and r["lenguaje"] == "Java"), None)
        r_p = next((r for r in sub if r["algoritmo"] == alg and r["lenguaje"] == "Python"), None)
        java_tiempos.append(r_j["tiempo_ms"] if r_j else 0)
        java_est.append(r_j["tipo"] == "estimado" if r_j else False)
        py_tiempos.append(r_p["tiempo_ms"] if r_p else 0)
        py_est.append(r_p["tipo"] == "estimado" if r_p else False)

    pos_java = x - ancho / 2
    pos_py = x + ancho / 2

    for p, t, est in zip(pos_java, java_tiempos, java_est):
        hatch = "//" if est else ""
        ax.bar(
            p,
            t,
            ancho,
            color="#2b5797",
            edgecolor="#112244" if est else "#2b5797",
            hatch=hatch,
            alpha=0.7 if est else 0.95,
        )
        if t > 0:
            texto = formato_tiempo(t) + ("*" if est else "")
            ax.annotate(
                texto,
                xy=(p, t),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=8,
                fontweight="bold",
            )

    for p, t, est in zip(pos_py, py_tiempos, py_est):
        hatch = "//" if est else ""
        ax.bar(
            p,
            t,
            ancho,
            color="#f39c12",
            edgecolor="#7a4e09" if est else "#f39c12",
            hatch=hatch,
            alpha=0.7 if est else 0.95,
        )
        if t > 0:
            texto = formato_tiempo(t) + ("*" if est else "")
            ax.annotate(
                texto,
                xy=(p, t),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=8,
                fontweight="bold",
            )

    handles = [
        mpatches.Patch(
            facecolor="#2b5797",
            edgecolor="#1a1a1a",
            linewidth=0.6,
            label="Java (Compilado / JIT)",
        ),
        mpatches.Patch(
            facecolor="#f39c12",
            edgecolor="#1a1a1a",
            linewidth=0.6,
            label="Python (Interpretado)",
        ),
    ]
    if any(py_est) or any(java_est):
        handles.append(
            mpatches.Patch(
                facecolor="#f2f2f2",
                edgecolor="#333333",
                hatch="//",
                linewidth=0.8,
                label="* Rayado: Estimado",
            )
        )

    ax.set_yscale("log")
    ax.set_ylabel("Tiempo de Ejecución (ms) [Escala Log]", fontsize=11, fontweight="bold")
    ax.set_title(
        "Punto 1: Comparativa Compilado (Java) vs Interpretado (Python)\n(n = 1.000.000 elementos, Entrada Aleatoria)",
        fontsize=13,
        fontweight="bold",
    )
    ax.set_xticks(x)
    ax.set_xticklabels(ALGORITMOS, rotation=15, ha="right", fontsize=10, fontweight="bold")
    ax.grid(axis="y", which="both", linestyle="--", alpha=0.45)
    ax.legend(
        handles=handles,
        loc="upper right",
        frameon=True,
        framealpha=0.92,
        edgecolor="#cccccc",
        fontsize=10,
    )

    y_max = max(max(java_tiempos), max(py_tiempos)) * 18.0
    y_min = min(min([t for t in java_tiempos if t > 0]), min([t for t in py_tiempos if t > 0])) * 0.3
    ax.set_ylim(y_min, y_max)

    plt.tight_layout()
    nombre_archivo = "comparativa_ordenamiento_java_vs_python_1m.png"
    ruta_guardado = DIR_GRAFICAS / nombre_archivo
    plt.savefig(ruta_guardado)
    plt.close()
    print(f"Gráfica generada: {ruta_guardado}")


def main():
    DIR_GRAFICAS.mkdir(parents=True, exist_ok=True)
    registros = cargar_registros()
    if not registros:
        print("No se encontraron registros en results/raw/.")
        return

    # 1. Gráficas de crecimiento (2 gráficas)
    graficar_crecimiento(registros, "Java")
    graficar_crecimiento(registros, "Python")

    # 2. Efecto del orden de entrada en Java (3 gráficas: 1000, 10000, 100000)
    graficar_efecto_orden(registros, 1_000)
    graficar_efecto_orden(registros, 10_000)
    graficar_efecto_orden(registros, 100_000)

    # 3. Compilado vs interpretado para n = 1.000.000 (1 gráfica)
    graficar_compilado_vs_interpretado(registros)


if __name__ == "__main__":
    main()
