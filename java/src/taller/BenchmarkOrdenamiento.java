package taller;

import java.io.IOException;
import java.nio.file.*;
import java.util.*;
import taller.sorting.*;
import taller.util.*;

public class BenchmarkOrdenamiento {

    static final int[] TAMANOS = { 1_000, 10_000, 100_000, 1_000_000 };
    static final String[] VARIANTES = { "aleatorio", "ascendente", "descendente" };
    static final int REPETICIONES = 5;
    static final long LIMITE_NS = 60_000_000_000L;
    static final int TAM_CALENTAMIENTO = 10_000;
    static final Path RAW = resolverDirRaw();
    static final Path INCIDENTES = RAW.resolve("incidentes_ordenamiento_java.csv");

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

        Ordenador[] algoritmos = {
                new InsertionSort(), new DualPivotQuickSort(), new MergeSort(),
                new HeapSort(), new RadixSort(), new BucketSort()
        };

        ResultadoCSV csv = new ResultadoCSV(RAW.resolve("ordenamiento_java.csv"), "Java");
        if (!Files.exists(INCIDENTES)) {
            Files.writeString(INCIDENTES, "algoritmo,lenguaje,variante,n,motivo\n");
        }

        Map<String, double[]> previo = new HashMap<>();
        Set<String> bloqueados = new HashSet<>();

        for (String variante : VARIANTES) {
            for (int n : TAMANOS) {
                if (n > maxN)
                    continue;
                int[] original = ArchivoUtil.leerArreglo(variante, n);

                for (Ordenador alg : algoritmos) {
                    String clave = alg.nombre() + "|" + variante;

                    if (bloqueados.contains(clave)) {
                        incidente(alg, variante, n, "omitido_por_n_menor");
                        double[] p = previo.get(clave);
                        if (p != null) {
                            double tEst = prediccion(alg, variante, p, n);
                            csv.escribirEstimado(alg.nombre(), variante, n, "NA", tEst);
                            System.out.printf(Locale.ROOT, "%-20s %-11s n=%-8d %12.3f ms (estimado)%n",
                                    alg.nombre(), variante, n, tEst / 1e6);
                        }
                        continue;
                    }
                    double[] p = previo.get(clave);
                    if (p != null) {
                        double tEst = prediccion(alg, variante, p, n);
                        if (tEst > LIMITE_NS) {
                            bloqueados.add(clave);
                            incidente(alg, variante, n, "timeout_previsto");
                            csv.escribirEstimado(alg.nombre(), variante, n, "NA", tEst);
                            System.out.printf(Locale.ROOT, "%-20s %-11s n=%-8d %12.3f ms (estimado timeout)%n",
                                    alg.nombre(), variante, n, tEst / 1e6);
                            continue;
                        }
                    }

                    long[] tiempos = new long[REPETICIONES];
                    String motivo = null;
                    try {
                        alg.ordenar(Arrays.copyOf(original, Math.min(n, TAM_CALENTAMIENTO)));

                        for (int r = 0; r < REPETICIONES; r++) {
                            int[] copia = original.clone();
                            long ini = System.nanoTime();
                            alg.ordenar(copia);
                            long dur = System.nanoTime() - ini;

                            if (!Verificador.verificar(original, copia)) {
                                throw new IllegalStateException("Resultado incorrecto: " + alg.nombre());
                            }
                            tiempos[r] = dur;
                            if (dur > LIMITE_NS) {
                                motivo = "excede_5_min(" + dur + "ns)";
                                break;
                            }
                        }
                    } catch (StackOverflowError e) {
                        motivo = "StackOverflowError";
                    }

                    if (motivo != null) {
                        bloqueados.add(clave);
                        incidente(alg, variante, n, motivo);
                        if (p != null) {
                            double tEst = prediccion(alg, variante, p, n);
                            csv.escribirEstimado(alg.nombre(), variante, n, "NA", tEst);
                            System.out.printf(Locale.ROOT, "%-20s %-11s n=%-8d %12.3f ms (estimado por error)%n",
                                    alg.nombre(), variante, n, tEst / 1e6);
                        }
                    } else {
                        csv.escribirMedido(alg.nombre(), variante, n, "NA", tiempos);
                        double prom = Arrays.stream(tiempos).average().orElse(0);
                        previo.put(clave, new double[] { n, prom });
                        System.out.printf(Locale.ROOT, "%-20s %-11s n=%-8d %12.3f ms%n",
                                alg.nombre(), variante, n, prom / 1e6);
                    }
                }
            }
        }
        System.out.println("Listo.");
    }

    static double prediccion(Ordenador alg, String variante, double[] prev, int n) {
        double r = (double) n / prev[0];
        boolean esCuadratico = (alg instanceof InsertionSort)
                || (alg instanceof DualPivotQuickSort
                        && ("ascendente".equals(variante) || "descendente".equals(variante)));
        double factor = esCuadratico
                ? r * r
                : r * Math.log(n) / Math.log(prev[0]);
        return prev[1] * factor;
    }

    static void incidente(Ordenador alg, String variante, int n, String motivo) throws IOException {
        String fila = String.join(",", alg.nombre(), "Java", variante, String.valueOf(n), motivo);
        Files.writeString(INCIDENTES, fila + "\n", StandardOpenOption.APPEND);
        System.out.println("  INCIDENTE: " + fila);
    }
}