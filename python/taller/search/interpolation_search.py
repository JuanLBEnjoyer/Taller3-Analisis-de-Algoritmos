NOMBRE = "InterpolationSearch"


def buscar(arr, x):
    lo = 0
    hi = len(arr) - 1

    while lo <= hi and x >= arr[lo] and x <= arr[hi]:
        if arr[hi] == arr[lo]:
            if arr[lo] == x:
                return lo
            return -1

        pos = lo + ((hi - lo) * (x - arr[lo])) // (arr[hi] - arr[lo])

        if arr[pos] == x:
            return pos
        if arr[pos] < x:
            lo = pos + 1
        else:
            hi = pos - 1

    return -1
