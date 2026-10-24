package taller.sorting;

public class InsertionSort implements Ordenador {
    public String nombre() {
        return "InsertionSort";
    }

    public void ordenar(int[] a) {
        for (int i = 1; i < a.length; i++) {
            int clave = a[i];
            int j = i - 1;
            while (j >= 0 && a[j] > clave) { // desplaza los mayores a la derecha
                a[j + 1] = a[j];
                j--;
            }
            a[j + 1] = clave;
        }
    }
}
