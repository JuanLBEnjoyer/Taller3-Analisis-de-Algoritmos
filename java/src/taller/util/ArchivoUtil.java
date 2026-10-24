package taller.util;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.stream.Stream;

public final class ArchivoUtil {

    private static final Path DIR_DATOS = Paths.get("data");

    private ArchivoUtil() {
    }

    public static int[] leerArreglo(String variante, int n) throws IOException {
        return leer(DIR_DATOS.resolve(variante + "_" + n + ".txt"));
    }

    public static int[] leerClaves(int n) throws IOException {
        return leer(DIR_DATOS.resolve("claves_busqueda_" + n + ".txt"));
    }

    public static int[] leerClavesPosicion(int n) throws IOException {
        return leer(DIR_DATOS.resolve("claves_posicion_" + n + ".txt"));
    }

    private static int[] leer(Path ruta) throws IOException {
        try (Stream<String> lineas = Files.lines(ruta)) {
            return lineas.map(String::trim)
                    .filter(s -> !s.isEmpty())
                    .mapToInt(Integer::parseInt)
                    .toArray();
        }
    }
}
