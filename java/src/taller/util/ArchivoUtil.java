package taller.util;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.stream.Stream;

public final class ArchivoUtil {

    private static Path obtenerDirDatos() {
        if (Files.exists(Paths.get("data"))) {
            return Paths.get("data");
        }
        if (Files.exists(Paths.get("..", "data"))) {
            return Paths.get("..", "data");
        }
        return Paths.get("data");
    }

    private static Path resolverRuta(int n, String nombreArchivo) {
        Path dir = obtenerDirDatos();
        Path conSubcarpeta = dir.resolve(String.valueOf(n)).resolve(nombreArchivo);
        if (Files.exists(conSubcarpeta)) {
            return conSubcarpeta;
        }
        return dir.resolve(nombreArchivo);
    }

    public static int[] leerArreglo(String variante, int n) throws IOException {
        return leer(resolverRuta(n, variante + "_" + n + ".txt"));
    }

    public static int[] leerClaves(int n) throws IOException {
        return leer(resolverRuta(n, "claves_busqueda_" + n + ".txt"));
    }

    public static int[] leerClavesPosicion(int n) throws IOException {
        return leer(resolverRuta(n, "claves_posicion_" + n + ".txt"));
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
