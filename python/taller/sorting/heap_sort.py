NOMBRE = "HeapSort"


def ordenar(a):
    n = len(a)
    for i in range(n // 2 - 1, -1, -1):
        _hundir(a, n, i)
    for fin in range(n - 1, 0, -1):
        a[0], a[fin] = a[fin], a[0]
        _hundir(a, fin, 0)


def _hundir(a, tam, i):
    while True:
        mayor, izq = i, 2 * i + 1
        der = izq + 1
        if izq < tam and a[izq] > a[mayor]:
            mayor = izq
        if der < tam and a[der] > a[mayor]:
            mayor = der
        if mayor == i:
            return
        a[i], a[mayor] = a[mayor], a[i]
        i = mayor