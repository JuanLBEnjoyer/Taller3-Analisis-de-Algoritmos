package taller.search;

public class ExponentialSearch implements Buscador {
    @Override
    public String nombre() {
        return "ExponentialSearch";
    }

    private int binarySearch(int[] arr, int low, int high, int x) {
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (arr[mid] == x) {
                return mid;
            }
            if (arr[mid] < x) {
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }
        return -1;
    }

    @Override
    public int buscar(int[] arr, int x) {
        int n = arr.length;
        if (n == 0) {
            return -1;
        }
        if (arr[0] == x) {
            return 0;
        }

        int i = 1;
        while (i < n && arr[i] <= x) {
            i *= 2;
        }

        return binarySearch(arr, i / 2, Math.min(i, n - 1), x);
    }
}
