package taller.util;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.util.Locale;

public class ResultadoCSV {

    private static final int REPETICIONES = 5;
    private static final String ENCABEZADO = "algoritmo,lenguaje,variante,n,posicion_clave,"
            + "rep1,rep2,rep3,rep4,rep5,promedio_ns,desv_std_ns,tipo";

    private final Path archivo;
    private final String lenguaje;

    public ResultadoCSV(Path archivo, String lenguaje) throws IOException {
        this.archivo = archivo;
        this.lenguaje = lenguaje;
        Files.createDirectories(archivo.getParent());
        if (!Files.exists(archivo)) {
            Files.writeString(archivo, ENCABEZADO + "\n");
        }
    }

    public void escribirMedido(String algoritmo, String variante, int n,
            String posicionClave, long[] tiempos) throws IOException {
        if (tiempos.length != REPETICIONES) {
            throw new IllegalArgumentException("Se esperaban " + REPETICIONES + " repeticiones");
        }
        double promedio = promedio(tiempos);
        double desv = desviacion(tiempos, promedio);

        StringBuilder sb = new StringBuilder();
        sb.append(String.join(",", algoritmo, lenguaje, variante,
                String.valueOf(n), posicionClave));
        for (long t : tiempos)
            sb.append(',').append(t);
        sb.append(',').append(String.format(Locale.ROOT, "%.1f", promedio));
        sb.append(',').append(String.format(Locale.ROOT, "%.1f", desv));
        sb.append(",medido\n");
        agregar(sb.toString());
    }

    public void escribirEstimado(String algoritmo, String variante, int n,
            String posicionClave, double promedioNs) throws IOException {
        String fila = String.join(",", algoritmo, lenguaje, variante,
                String.valueOf(n), posicionClave,
                "", "", "", "", "",
                String.format(Locale.ROOT, "%.1f", promedioNs),
                "", "estimado") + "\n";
        agregar(fila);
    }

    private void agregar(String fila) throws IOException {
        Files.writeString(archivo, fila, StandardOpenOption.APPEND);
    }

    private static double promedio(long[] t) {
        double suma = 0;
        for (long x : t)
            suma += x;
        return suma / t.length;
    }

    private static double desviacion(long[] t, double promedio) {
        double suma = 0;
        for (long x : t)
            suma += (x - promedio) * (x - promedio);
        return Math.sqrt(suma / (t.length - 1));
    }
}