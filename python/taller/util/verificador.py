def esta_ordenado(a):
    return all(a[i - 1] <= a[i] for i in range(1, len(a)))


def verificar(original, resultado):
    return esta_ordenado(resultado) and sorted(original) == resultado