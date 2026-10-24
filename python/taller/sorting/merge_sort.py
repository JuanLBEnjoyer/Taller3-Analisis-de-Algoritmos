NOMBRE = "MergeSort"


def ordenar(a):
    aux = [0] * len(a)
    _ordenar(a, aux, 0, len(a) - 1)


def _ordenar(a, aux, izq, der):
    if izq >= der:
        return
    medio = izq + (der - izq) // 2
    _ordenar(a, aux, izq, medio)
    _ordenar(a, aux, medio + 1, der)
    _mezclar(a, aux, izq, medio, der)


def _mezclar(a, aux, izq, medio, der):
    aux[izq:der + 1] = a[izq:der + 1]
    i, j, k = izq, medio + 1, izq
    while i <= medio and j <= der:
        if aux[i] <= aux[j]:
            a[k] = aux[i]
            i += 1
        else:
            a[k] = aux[j]
            j += 1
        k += 1
    while i <= medio:
        a[k] = aux[i]
        i += 1
        k += 1
    while j <= der:
        a[k] = aux[j]
        j += 1
        k += 1