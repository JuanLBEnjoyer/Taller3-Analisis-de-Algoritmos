NOMBRE = "RadixSort"


def ordenar(a):
    if len(a) < 2:
        return
    maximo = a[0]
    for v in a:
        if v > maximo:
            maximo = v

    salida = [0] * len(a)
    exp = 1
    while maximo // exp > 0:
        _conteo(a, salida, exp)
        exp *= 10


def _conteo(a, salida, exp):
    cuenta = [0] * 10
    for v in a:
        cuenta[(v // exp) % 10] += 1
    for d in range(1, 10):
        cuenta[d] += cuenta[d - 1]
    for i in range(len(a) - 1, -1, -1):
        d = (a[i] // exp) % 10
        cuenta[d] -= 1
        salida[cuenta[d]] = a[i]
    a[:] = salida