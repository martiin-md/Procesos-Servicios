/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package act4pspsuspenderfile;

/**
 *
 * @author martin
 */
public class SolicitaSuspender {

    boolean suspendido = false;

    public synchronized void set(boolean suspendido) {
        this.suspendido = suspendido;
        if (!suspendido) {
            notifyAll();

        }
    }

    public synchronized void esperandoParaReanudar() throws InterruptedException {
        while (suspendido) { 
            wait(); 
        }
    }
}
