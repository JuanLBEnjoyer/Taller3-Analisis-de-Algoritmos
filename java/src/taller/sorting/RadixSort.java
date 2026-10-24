package taller.sorting;

public class RadixSort implements Ordenador {
    public String nombre() {
        return "RadixSort";
    }

    public void ordenar(int[] a) {
        if (a.length < 2)
            return;
        int max = a[0];
        for (int v : a)
            if (v > max)
                max = v;

        int[] salida = new int[a.length];
        for (long exp = 1; max / exp > 0; exp *= 10) {
            conteo(a, salida, exp);
        }
    }

    private void conteo(int[] a, int[] salida, long exp) {
        int[] cuenta = new int[10];
        for (int v : a)
            cuenta[(int) ((v / exp) % 10)]++;
        for (int d = 1; d < 10; d++)
            cuenta[d] += cuenta[d - 1];
        for (int i = a.length - 1; i >= 0; i--) {
            int d = (int) ((a[i] / exp) % 10);
            salida[--cuenta[d]] = a[i];
        }
        System.arraycopy(salida, 0, a, 0, a.length);
    }
}
