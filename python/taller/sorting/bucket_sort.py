NOMBRE = "BucketSort"


def ordenar(a):
    n = len(a)
    if n < 2:
        return
    minimo, maximo = a[0], a[0]
    for v in a:
        if v < minimo:
            minimo = v
        if v > maximo:
            maximo = v
    if minimo == maximo:
        return

    k = n
    rango = maximo - minimo + 1

    inicio = [0] * (k + 1)
    for v in a:
        inicio[(v - minimo) * k // rango + 1] += 1
    for b in range(k):
        inicio[b + 1] += inicio[b]

    siguiente = inicio[:k]
    salida = [0] * n
    for v in a:
        b = (v - minimo) * k // rango
        salida[siguiente[b]] = v
        siguiente[b] += 1

    for b in range(k):
        _insertion(salida, inicio[b], inicio[b + 1] - 1)
    a[:] = salida


def _insertion(a, izq, der):
    for i in range(izq + 1, der + 1):
        clave = a[i]
        j = i - 1
        while j >= izq and a[j] > clave:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = clave