NOMBRE = "ExponentialSearch"


def _binary_search(arr, low, high, x):
    while low <= high:
        mid = low + (high - low) // 2
        if arr[mid] == x:
            return mid
        if arr[mid] < x:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def buscar(arr, x):
    n = len(arr)
    if n == 0:
        return -1
    if arr[0] == x:
        return 0

    i = 1
    while i < n and arr[i] <= x:
        i *= 2

    return _binary_search(arr, i // 2, min(i, n - 1), x)
