NOMBRE = "DualPivotQuickSort"


def ordenar(a):
    _ordenar(a, 0, len(a) - 1)


def _ordenar(a, bajo, alto):
    if bajo >= alto:
        return
    if a[bajo] > a[alto]:
        a[bajo], a[alto] = a[alto], a[bajo]

    p, q = a[bajo], a[alto]
    lt, gt, i = bajo + 1, alto - 1, bajo + 1

    while i <= gt:
        if a[i] < p:
            a[i], a[lt] = a[lt], a[i]
            lt += 1
            i += 1
        elif a[i] > q:
            a[i], a[gt] = a[gt], a[i]
            gt -= 1
        else:
            i += 1

    lt -= 1
    gt += 1
    a[bajo], a[lt] = a[lt], a[bajo]
    a[alto], a[gt] = a[gt], a[alto]

    _ordenar(a, bajo, lt - 1)
    _ordenar(a, lt + 1, gt - 1)
    _ordenar(a, gt + 1, alto)