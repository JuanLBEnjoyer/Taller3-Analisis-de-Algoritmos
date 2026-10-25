package taller;

import java.nio.file.*;
import java.util.*;
import taller.search.*;
import taller.util.*;

public class BenchmarkBusqueda {

    static final int[] TAMANOS = { 1_000, 10_000, 100_000, 1_000_000 };
    static final int REPETICIONES = 5;
    static final Path RAW = resolverDirRaw();

    private static Path resolverDirRaw() {
        if (Files.exists(Paths.get("results"))) {
            return Paths.get("results", "raw");
        }
        if (Files.exists(Paths.get("..", "results"))) {
            return Paths.get("..", "results", "raw");
        }
        return Paths.get("results", "raw");
    }

    public static void main(String[] args) throws Exception {
        int maxN = args.length > 0 ? Integer.parseInt(args[0]) : Integer.MAX_VALUE;

        Buscador[] algoritmos = {
                new LinearSearch(),
                new BinarySearch(),
                new TernarySearch(),
                new JumpSearch(),
                new InterpolationSearch(),
                new ExponentialSearch()
        };

        ResultadoCSV csv = new ResultadoCSV(RAW.resolve("busqueda_java.csv"), "Java");

        // Calentamiento JIT con arreglo de 10.000 elementos
        int[] arrCalentamiento = ArchivoUtil.leerArreglo("ascendente", 10_000);
        int[] clavesCalentamiento = ArchivoUtil.leerClaves(10_000);
        for (Buscador alg : algoritmos) {
            for (int i = 0; i < 200; i++) {
                alg.buscar(arrCalentamiento, clavesCalentamiento[i % clavesCalentamiento.length]);
            }
        }

        System.out.println("=== EXPERIMENTO 1: Crecimiento con 1.000 claves (500 presentes, 500 ausentes) ===");
        for (int n : TAMANOS) {
            if (n > maxN)
                continue;
            int[] arr = ArchivoUtil.leerArreglo("ascendente", n);
            int[] claves = ArchivoUtil.leerClaves(n);
            int numClaves = claves.length;

            for (Buscador alg : algoritmos) {
                long[] tiempos = new long[REPETICIONES];

                for (int r = 0; r < REPETICIONES; r++) {
                    long ini = System.nanoTime();
                    for (int x : claves) {
                        alg.buscar(arr, x);
                    }
                    long dur = System.nanoTime() - ini;
                    tiempos[r] = dur / numClaves; // ns por búsqueda
                }

                csv.escribirMedido(alg.nombre(), "ascendente", n, "general_1000", tiempos);
                double prom = Arrays.stream(tiempos).average().orElse(0);
                System.out.printf(Locale.ROOT, "%-20s n=%-8d %10.1f ns/búsqueda (%7.3f µs)%n",
                        alg.nombre(), n, prom, prom / 1000.0);
            }
        }

        System.out.println("\n=== EXPERIMENTO 2: Posición de clave (inicio, centro, final) para n = 1.000.000 ===");
        if (1_000_000 <= maxN) {
            int[] arr1M = ArchivoUtil.leerArreglo("ascendente", 1_000_000);
            int[] clavesPos = ArchivoUtil.leerClavesPosicion(1_000_000);
            String[] nombresPos = { "inicio", "centro", "final" };

            for (int p = 0; p < 3; p++) {
                String posNombre = nombresPos[p];
                int clave = clavesPos[p];

                for (Buscador alg : algoritmos) {
                    long[] tiempos = new long[REPETICIONES];

                    for (int r = 0; r < REPETICIONES; r++) {
                        long ini = System.nanoTime();
                        for (int k = 0; k < 1000; k++) {
                            alg.buscar(arr1M, clave);
                        }
                        long dur = System.nanoTime() - ini;
                        tiempos[r] = dur / 1000; // ns por búsqueda
                    }

                    csv.escribirMedido(alg.nombre(), "ascendente", 1_000_000, posNombre, tiempos);
                    double prom = Arrays.stream(tiempos).average().orElse(0);
                    System.out.printf(Locale.ROOT, "%-20s pos=%-7s %10.1f ns/búsqueda (%7.3f µs)%n",
                            alg.nombre(), posNombre, prom, prom / 1000.0);
                }
            }
        }

        System.out.println("\nListo benchmark de búsqueda Java.");
    }
}
