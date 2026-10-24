package taller.sorting;

public class HeapSort implements Ordenador {
    public String nombre() {
        return "HeapSort";
    }

    public void ordenar(int[] a) {
        int n = a.length;
        for (int i = n / 2 - 1; i >= 0; i--)
            hundir(a, n, i);
        for (int fin = n - 1; fin > 0; fin--) {
            intercambiar(a, 0, fin);
            hundir(a, fin, 0);
        }
    }

    private void hundir(int[] a, int tam, int i) {
        while (true) {
            int mayor = i, izq = 2 * i + 1, der = izq + 1;
            if (izq < tam && a[izq] > a[mayor])
                mayor = izq;
            if (der < tam && a[der] > a[mayor])
                mayor = der;
            if (mayor == i)
                return;
            intercambiar(a, i, mayor);
            i = mayor;
        }
    }

    private static void intercambiar(int[] a, int i, int j) {
        int t = a[i];
        a[i] = a[j];
        a[j] = t;
    }
}