package taller;

import java.util.Random;
import taller.sorting.*;
import taller.util.Verificador;

public class PruebaOrdenamiento {
    public static void main(String[] args) {
        Ordenador[] algoritmos = {
                new InsertionSort(), new DualPivotQuickSort(), new MergeSort(),
                new HeapSort(), new RadixSort(), new BucketSort()
        };
        int[] tamanos = { 0, 1, 2, 5, 50, 300 };
        Random rnd = new Random(1);

        for (Ordenador alg : algoritmos) {
            boolean ok = true;
            for (int n : tamanos) {
                for (int caso = 0; caso < 4; caso++) {
                    int[] original = new int[n];
                    for (int i = 0; i < n; i++) {
                        original[i] = (caso == 3)
                                ? 10_000_000 + rnd.nextInt(5) // muchos duplicados
                                : 10_000_000 + rnd.nextInt(90_000_000);
                    }
                    if (caso == 1)
                        java.util.Arrays.sort(original);
                    if (caso == 2) {
                        java.util.Arrays.sort(original);
                        for (int i = 0; i < n / 2; i++) {
                            int t = original[i];
                            original[i] = original[n - 1 - i];
                            original[n - 1 - i] = t;
                        }
                    }
                    int[] copia = original.clone();
                    alg.ordenar(copia);
                    if (!Verificador.verificar(original, copia)) {
                        ok = false;
                        System.out.println("FALLO: " + alg.nombre() + " n=" + n + " caso=" + caso);
                    }
                }
            }
            System.out.println(alg.nombre() + ": " + (ok ? "OK" : "CON ERRORES"));
        }
    }
}