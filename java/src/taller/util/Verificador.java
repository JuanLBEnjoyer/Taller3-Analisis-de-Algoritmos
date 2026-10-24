package taller.util;

import java.util.Arrays;

public final class Verificador {

    private Verificador() {
    }

    public static boolean estaOrdenado(int[] a) {
        for (int i = 1; i < a.length; i++) {
            if (a[i - 1] > a[i])
                return false;
        }
        return true;
    }

    public static boolean verificar(int[] original, int[] resultado) {
        if (!estaOrdenado(resultado))
            return false;
        int[] referencia = original.clone();
        Arrays.sort(referencia);
        return Arrays.equals(referencia, resultado);
    }
}