/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package Ftp2;

import java.io.IOException;
import org.apache.commons.net.ftp.FTPClient;
import org.apache.commons.net.ftp.FTPReply;

/**
 *
 * @author martin
 */
public class Act1 {

    public static void main(String[] args) throws IOException {
        FTPClient cliente = new FTPClient();
        String servidor = "127.0.0.1"; 
        int puerto = 21; 
        String usuario = "user1";
        String contrasena = "1234"; 
        
        try {
            // Conexión al servidor FTP
            System.out.println("Nos conectamos a: " + servidor);
            cliente.connect(servidor, puerto);

            // Verifico la  respuesta del servidor
            int respuesta = cliente.getReplyCode();
            if (!FTPReply.isPositiveCompletion(respuesta)) {
                System.out.println("Conexión rechazada. Código: " + respuesta);
                cliente.disconnect();
                return;
            }

            // Se inicia sesión
            if (!cliente.login(usuario, contrasena)) {
                System.out.println("Inicio de sesión fallido.");
                cliente.logout();
                cliente.disconnect();
                return;
            }
            System.out.println("Login correcto...");

            // despue se imprime el directorio actual
            System.out.println("Directorio actual: " + cliente.printWorkingDirectory());

            // y se intenta crear un directorio en user1
            cliente.changeWorkingDirectory("/user1");
            if (cliente.makeDirectory("PruebaEscribir")) {
                System.out.println("Directorio creado exitosamente en user1.");
            } else {
                System.out.println("Fallo al crear directorio en Usuario1. Código de respuesta: " + cliente.getReplyCode());
            }

            // después se crea un directorio en user2
            cliente.changeWorkingDirectory("/user2");
            if (cliente.makeDirectory("PruebaEscribir")) {
                System.out.println("Directorio creado exitosamente en user2.");
            } else {
                System.out.println("Fallo al crear directorio en Usuario2. Código de respuesta: " + cliente.getReplyCode());
            }

            // y le cambiamos al directorio raíz para listar los archivos
            cliente.changeWorkingDirectory("/FTPServer");
            System.out.println("Dir Actual:" + cliente.printWorkingDirectory());

            // aqui listo los ficheros y directorios
            var archivos = cliente.listFiles();
            System.out.println("Ficheros en el directorio actual:" + archivos.length);
            for (var archivo : archivos) {
                System.out.print(" " + archivo.getName() + " => ");
                System.out.println(archivo.isDirectory() ? "Directorio" : "Fichero");
            }

            // Finalmente se cierra sesión y se desconecta
            cliente.logout();
            System.out.println("Se ha cerrado sesion del servidor FTP...");
            cliente.disconnect();
            System.out.println("Desconectado..");

        } catch (IOException e) {
            System.out.println("Error de E/S: " + e.getMessage());
        }
    }
}
