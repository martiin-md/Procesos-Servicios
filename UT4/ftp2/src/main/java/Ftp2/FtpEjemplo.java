package Ftp2;

import java.io.IOException;
import java.net.SocketException;
import org.apache.commons.net.ftp.FTPClient;
import org.apache.commons.net.ftp.FTPReply;

/**
 * Clase principal para conectarse a un servidor FTP.
 *
 * @author marti
 */
public class FtpEjemplo {

    public static void main(String[] args) throws SocketException, IOException {
        FTPClient cliente = new FTPClient();
        String servFTP = "ftp.rediris.es"; // servidor FTP

        System.out.println("Nos conectamos a: " + servFTP);
        cliente.connect(servFTP);

        // Respuesta del servidor FTP
        System.out.print(cliente.getReplyString());

        // Código de respuesta
        int respuesta = cliente.getReplyCode();
        System.out.println("Respuesta: " + respuesta);

        // Comprobación del código de respuesta
        if (!FTPReply.isPositiveCompletion(respuesta)) {
            cliente.disconnect();
            System.out.println("Conexión rechazada: " + respuesta);
            System.exit(0);
        }
        // Desconexión del servidor FTP
        cliente.disconnect();
        System.out.println("Conexión finalizada.");
    }
}