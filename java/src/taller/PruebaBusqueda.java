package taller;

import java.util.Arrays;
import java.util.Random;
import taller.search.*;

public class PruebaBusqueda {
    public static void main(String[] args) {
        Buscador[] algoritmos = {
                new LinearSearch(),
                new BinarySearch(),
                new TernarySearch(),
                new JumpSearch(),
                new InterpolationSearch(),
                new ExponentialSearch()
        };

        int[] tamanos = { 0, 1, 2, 5, 20, 100, 1000 };
        Random rnd = new Random(42);

        for (Buscador alg : algoritmos) {
            boolean ok = true;
            for (int n : tamanos) {
                int[] arr = new int[n];
                for (int i = 0; i < n; i++) {
                    arr[i] = 10_000_000 + rnd.nextInt(90_000_000);
                }
                Arrays.sort(arr);

                // Probar presentes
                int repPresentes = Math.min(n, 10);
                for (int i = 0; i < repPresentes; i++) {
                    int idx = rnd.nextInt(n);
                    int val = arr[idx];
                    int res = alg.buscar(arr, val);
                    if (res < 0 || res >= n || arr[res] != val) {
                        ok = false;
                        System.out.printf("FALLO presente: %s n=%d val=%d res=%d%n", alg.nombre(), n, val, res);
                        break;
                    }
                }

                // Probar ausentes
                for (int i = 0; i < 10; i++) {
                    int val = 10_000_000 + rnd.nextInt(90_000_000);
                    if (Arrays.binarySearch(arr, val) < 0) {
                        int res = alg.buscar(arr, val);
                        if (res != -1) {
                            ok = false;
                            System.out.printf("FALLO ausente: %s n=%d val=%d res=%d%n", alg.nombre(), n, val, res);
                            break;
                        }
                    }
                }

                // Probar extremos
                if (n > 0) {
                    int[] extremos = { arr[0], arr[n / 2], arr[n - 1] };
                    for (int val : extremos) {
                        int res = alg.buscar(arr, val);
                        if (res == -1 || arr[res] != val) {
                            ok = false;
                            System.out.printf("FALLO extremo: %s n=%d val=%d res=%d%n", alg.nombre(), n, val, res);
                            break;
                        }
                    }
                }
            }
            System.out.println(alg.nombre() + ": " + (ok ? "OK" : "CON ERRORES"));
        }
    }
}
