/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package ExUT2MultiHiloEjercicio1;

/**
 *
 * @author martin
 */
public class CompradorEntradas extends Thread {

    private static int contador = 0; // Contador estatico para asignar un ID unico a cada comprador
    private int idComprador; 
    private Cola colaEntradas; 

    // Constructor que inicializa la cola de entradas y asigna un ID unico al comprador
    public CompradorEntradas(Cola colaEntradas) {
        this.colaEntradas = colaEntradas;
        this.idComprador = ++contador; // Incrementa el contador y asigna el valor al ID del comprador
    }

    // Metodo run que se ejecuta cuando el hilo empieza
    @Override
    public void run() {
        Entrada entrada = colaEntradas.getEntrada(); 
        if (entrada != null) {
            // Si hay una entrada disponible imprime el mensaje con el ID del comprador y la entrada
            System.out.println("Comprador " + idComprador + " ha comprado: " + entrada);
        } else {
            System.out.println("No hay entradas disponibles para el Comprador " + idComprador);
        }
    }
}
