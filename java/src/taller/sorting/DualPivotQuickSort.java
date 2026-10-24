package taller.sorting;

public class DualPivotQuickSort implements Ordenador {
    public String nombre() {
        return "DualPivotQuickSort";
    }

    public void ordenar(int[] a) {
        ordenar(a, 0, a.length - 1);
    }

    private void ordenar(int[] a, int bajo, int alto) {
        if (bajo >= alto)
            return;
        if (a[bajo] > a[alto])
            intercambiar(a, bajo, alto);

        int p = a[bajo];
        int q = a[alto];
        int lt = bajo + 1;
        int gt = alto - 1;
        int i = bajo + 1;

        while (i <= gt) {
            if (a[i] < p) {
                intercambiar(a, i, lt);
                lt++;
                i++;
            } else if (a[i] > q) {
                intercambiar(a, i, gt);
                gt--;
            } else {
                i++;
            }
        }
        lt--;
        gt++;
        intercambiar(a, bajo, lt);
        intercambiar(a, alto, gt);

        ordenar(a, bajo, lt - 1);
        ordenar(a, lt + 1, gt - 1);
        ordenar(a, gt + 1, alto);
    }

    private static void intercambiar(int[] a, int i, int j) {
        int t = a[i];
        a[i] = a[j];
        a[j] = t;
    }
}
