package taller.search;

public class LinearSearch implements Buscador {
    @Override
    public String nombre() {
        return "LinearSearch";
    }

    @Override
    public int buscar(int[] arr, int x) {
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == x) {
                return i;
            }
        }
        return -1;
    }
}