/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package Act2;

/**
 *
 * @author martin
 */
public class SolicitaSuspender {
    private boolean suspender;

    // Establece el valor de la variable `suspender` y notifica a todos los hilos que esperan.
    public synchronized void set(boolean b) {
        suspender = b; // Actualiza el estado de la suspensión.
        notifyAll(); // Notifica a los hilos en espera para que revisen el estado.
    }

    // Pone el hilo en espera si `suspender` es verdadero.
    public synchronized void esperandoParaReanudar() throws InterruptedException {
        while (suspender) { // Mientras esté suspendido...
            wait(); // El hilo entra en espera.
        }
    }
}
