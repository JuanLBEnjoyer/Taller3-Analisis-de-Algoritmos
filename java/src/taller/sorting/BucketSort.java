package taller.sorting;

public class BucketSort implements Ordenador {
    public String nombre() {
        return "BucketSort";
    }

    public void ordenar(int[] a) {
        int n = a.length;
        if (n < 2)
            return;
        int min = a[0], max = a[0];
        for (int v : a) {
            if (v < min)
                min = v;
            if (v > max)
                max = v;
        }
        if (min == max)
            return;

        int k = n;
        long rango = (long) max - min + 1;

        int[] inicio = new int[k + 1];
        for (int v : a)
            inicio[indice(v, min, rango, k) + 1]++;
        for (int b = 0; b < k; b++)
            inicio[b + 1] += inicio[b];

        int[] siguiente = java.util.Arrays.copyOf(inicio, k);
        int[] salida = new int[n];
        for (int v : a)
            salida[siguiente[indice(v, min, rango, k)]++] = v;

        for (int b = 0; b < k; b++)
            insertion(salida, inicio[b], inicio[b + 1] - 1);
        System.arraycopy(salida, 0, a, 0, n);
    }

    private static int indice(int v, int min, long rango, int k) {
        return (int) (((long) (v - min) * k) / rango);
    }

    private static void insertion(int[] a, int izq, int der) {
        for (int i = izq + 1; i <= der; i++) {
            int clave = a[i], j = i - 1;
            while (j >= izq && a[j] > clave) {
                a[j + 1] = a[j];
                j--;
            }
            a[j + 1] = clave;
        }
    }
}