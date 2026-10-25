package taller.search;

public class JumpSearch implements Buscador {
    @Override
    public String nombre() {
        return "JumpSearch";
    }

    @Override
    public int buscar(int[] arr, int x) {
        int n = arr.length;
        if (n == 0) {
            return -1;
        }

        int blockSize = (int) Math.sqrt(n);
        if (blockSize == 0) {
            blockSize = 1;
        }

        int step = blockSize;
        int prev = 0;

        while (prev < n && arr[Math.min(step, n) - 1] < x) {
            prev = step;
            step += blockSize;
            if (prev >= n) {
                return -1;
            }
        }

        int limit = Math.min(step, n);
        while (prev < limit) {
            if (arr[prev] == x) {
                return prev;
            }
            if (arr[prev] > x) {
                return -1;
            }
            prev++;
        }

        return -1;
    }
}
