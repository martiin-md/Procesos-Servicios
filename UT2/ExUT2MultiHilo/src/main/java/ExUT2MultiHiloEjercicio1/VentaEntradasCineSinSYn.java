/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package ExUT2MultiHiloEjercicio1;

/**
 *
 * @author martin
 */
public class VentaEntradasCineSinSYn {

    public static void main(String[] args) {
        Cola colaEntradas = new Cola(5); // creo la cola comoo max 5
        GeneradorEntradas generador = new GeneradorEntradas(colaEntradas); // despues creo un generador de entradas y le pasa la cola
        generador.start(); 

        try {
            generador.join(); // Espera a que el generador termine de generar las entradas
        } catch (InterruptedException e) {
            e.printStackTrace(); // Maneja la excepción si el hilo es interrumpido
        }

        // Crea y empieza 6 hilos de compradores de entradas
        for (int i = 0; i < 6; i++) {
            new CompradorEntradas(colaEntradas).start();
        }
    }
}


