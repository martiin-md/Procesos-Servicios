/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package ExUT2MultiHiloEjercicio2;

/**
 *
 * @author martin
 */
public class ImprimirCadena {

    private int turno = 1; // Se define para asegurar el orden de impresión de los hilos

    public synchronized void PintaCadena(String s, int miTurno) {
        // Mientras no sea el turno....
        while (turno != miTurno) {
            try {
                wait();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }

        System.out.println(s);
        turno = (turno % 3) + 1; 
        notifyAll(); // Notifico despues a todos los hilos para que verifiquen su turno
    }
}
