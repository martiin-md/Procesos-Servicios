/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 */
package com.mycompany.testinetaddressej2psp;

import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;
import java.util.Map;

/**
 *
 * @author martin
 */
public class TestInetAddressEj2psp {

    public static void main(String[] args) {

        try {
            System.out.println("Constructor simple para una URL:");
            URL url = new URL("http://localhost/PFC/gest/cli_gestion.php?S=3");
            visualizar(url);
            obtenerInformacionDeConexion(url);

            System.out.println("Otro constructor simple para una URL:");
            url = new URL("http://docs.oracle.com");
            visualizar(url);
            obtenerInformacionDeConexion(url);

            System.out.println("Constructor para protocolo, URL y directorio:");
            url = new URL("http", "docs.oracle.com", "/javase/10");
            visualizar(url);
            obtenerInformacionDeConexion(url);

            System.out.println("Constructor para protocolo, URL, puerto y directorio:");
            url = new URL("http", "localhost", 8084, "/WebApp/Controlador?accion=modificar");
            visualizar(url);
            obtenerInformacionDeConexion(url);

            System.out.println("Constructor para un objeto URL en un contexto:");
            URL urlBase = new URL("http://docs.oracle.com/");
            url = new URL(urlBase, "/javase/10/docs/api/java/net/URL.html");
            visualizar(url);
            obtenerInformacionDeConexion(url);

        } catch (MalformedURLException e) {
            System.out.println("Error en la URL: " + e);
        } catch (IOException e) {
            System.out.println("Error en la conexión: " + e);
        }
    }

    // Método para visualizar la información básica de la URL
    private static void visualizar(URL url) {
        System.out.println("\tURL completa: " + url.toString());
        System.out.println("\tgetProtocol(): " + url.getProtocol());
        System.out.println("\tgetHost(): " + url.getHost());
        System.out.println("\tgetPort(): " + url.getPort());
        System.out.println("\tgetPath(): " + url.getPath());
        System.out.println("\tgetQuery(): " + url.getQuery());
    }

    // Método para obtener más detalles de la conexión URL
    private static void obtenerInformacionDeConexion(URL url) throws IOException {
        URLConnection connection = url.openConnection();

        // Obtener la URL de la conexión
        System.out.println("\tgetURL(): " + connection.getURL());

        // Obtener la última modificación del recurso
        System.out.println("\tgetLastModified(): " + connection.getLastModified());

        // Obtener el tipo de contenido
        System.out.println("\tgetContentType(): " + connection.getContentType());

        // Obtener las cabeceras de la respuesta
        Map<String, java.util.List<String>> headers = connection.getHeaderFields();
        System.out.println("\tgetHeaderFields(): ");
        for (Map.Entry<String, java.util.List<String>> entry : headers.entrySet()) {
            System.out.println("\t\t" + entry.getKey() + ": " + entry.getValue());
        }

        // Obtener el archivo de la URL
        System.out.println("\tgetFile(): " + connection.getURL().getFile());
    }

}
