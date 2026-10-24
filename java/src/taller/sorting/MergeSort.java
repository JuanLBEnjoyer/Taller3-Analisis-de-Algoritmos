package taller.sorting;

public class MergeSort implements Ordenador {
    public String nombre() {
        return "MergeSort";
    }

    public void ordenar(int[] a) {
        int[] aux = new int[a.length];
        ordenar(a, aux, 0, a.length - 1);
    }

    private void ordenar(int[] a, int[] aux, int izq, int der) {
        if (izq >= der)
            return;
        int medio = izq + (der - izq) / 2;
        ordenar(a, aux, izq, medio);
        ordenar(a, aux, medio + 1, der);
        mezclar(a, aux, izq, medio, der);
    }

    private void mezclar(int[] a, int[] aux, int izq, int medio, int der) {
        System.arraycopy(a, izq, aux, izq, der - izq + 1);
        int i = izq, j = medio + 1, k = izq;
        while (i <= medio && j <= der) {
            if (aux[i] <= aux[j])
                a[k++] = aux[i++];
            else
                a[k++] = aux[j++];
        }
        while (i <= medio)
            a[k++] = aux[i++];
        while (j <= der)
            a[k++] = aux[j++];
    }
}