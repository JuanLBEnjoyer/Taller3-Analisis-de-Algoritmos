import math

NOMBRE = "JumpSearch"


def buscar(arr, x):
    n = len(arr)
    if n == 0:
        return -1

    step = int(math.isqrt(n))
    if step == 0:
        step = 1

    prev = 0
    while prev < n and arr[min(step, n) - 1] < x:
        prev = step
        step += int(math.isqrt(n))
        if prev >= n:
            return -1

    while prev < min(step, n):
        if arr[prev] == x:
            return prev
        if arr[prev] > x:
            return -1
        prev += 1

    return -1
