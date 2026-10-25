package taller.search;

public class TernarySearch implements Buscador {
    @Override
    public String nombre() {
        return "TernarySearch";
    }

    @Override
    public int buscar(int[] arr, int x) {
        int l = 0;
        int r = arr.length - 1;

        while (l <= r) {
            int mid1 = l + (r - l) / 3;
            int mid2 = r - (r - l) / 3;

            if (arr[mid1] == x) {
                return mid1;
            }
            if (arr[mid2] == x) {
                return mid2;
            }

            if (x < arr[mid1]) {
                r = mid1 - 1;
            } else if (x > arr[mid2]) {
                l = mid2 + 1;
            } else {
                l = mid1 + 1;
                r = mid2 - 1;
            }
        }
        return -1;
    }
}
