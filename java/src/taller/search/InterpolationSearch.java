package taller.search;

public class InterpolationSearch implements Buscador {
    @Override
    public String nombre() {
        return "InterpolationSearch";
    }

    @Override
    public int buscar(int[] arr, int x) {
        int lo = 0;
        int hi = arr.length - 1;

        while (lo <= hi && x >= arr[lo] && x <= arr[hi]) {
            if (arr[hi] == arr[lo]) {
                if (arr[lo] == x) {
                    return lo;
                }
                return -1;
            }

            // Uso de long para prevenir desbordamiento aritmético con claves de 8 dígitos y n grande
            int pos = lo + (int) (((long) (hi - lo) * (x - arr[lo])) / (arr[hi] - arr[lo]));

            if (arr[pos] == x) {
                return pos;
            }
            if (arr[pos] < x) {
                lo = pos + 1;
            } else {
                hi = pos - 1;
            }
        }

        return -1;
    }
}