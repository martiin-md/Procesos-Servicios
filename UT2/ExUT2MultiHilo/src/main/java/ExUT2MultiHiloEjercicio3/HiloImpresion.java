/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package ExUT2MultiHiloEjercicio3;

/**
 *
 * @author martin
 */
public class HiloImpresion extends Thread {

    private volatile boolean detenerImpresion = false; 
    private volatile boolean suspendido = false; 
    private int contador = 0; 

    private SolicitaValor solicitaValorSuspender; 

    // Constructor que inicializa el objeto SolicitaSuspender.
    public HiloImpresion(SolicitaValor solicitaValorSuspender) {
        this.solicitaValorSuspender = solicitaValorSuspender;
    }


    // Se detiene el hilo estableciendo
    public void finalizarPrograama() {
        detenerImpresion = true;
        System.out.println("Final del PROGRAMA");
    }

    // Se suspende el hilo estableciendo
    public void suspenderHilo() {
        suspendido = true; 
        System.out.println("Fin bucle: " + contador);
        solicitaValorSuspender.set(true); // Activa la suspensión.
    }

    // Se reanuda el hilo estableciendo 
    public void reanudarHilo() {
        suspendido = false; 
        solicitaValorSuspender.set(false); // Activa la reanudación.
    }

    // Devuelve despues  el valor actual del contador.
    public int getContador() {
        return contador;
    }

    // Metodo principal del hilo.
    @Override
    public void run() {
        while (!detenerImpresion) { 
            contador++; // Se Incrementa el valor del contador.
            System.out.println("Hilo: " + contador);

            try {
                Thread.sleep(1000); // La Pausa de 1 segundo.
                solicitaValorSuspender.esperaReanundar();// Y después verifica si se debe suspender.
            } catch (InterruptedException e) {
                
                Thread.currentThread().interrupt();
            }
        }
        System.out.println("Final del Programa");
    }
}
