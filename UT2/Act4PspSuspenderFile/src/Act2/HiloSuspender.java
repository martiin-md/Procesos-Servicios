package Act2;

/**
 *
 * @author martin
 */
public class HiloSuspender extends Thread {

    // Variables controladoras del estado del hilo.
    private volatile boolean detener = false; 
    private volatile boolean suspendido = false; 
    private int contador = 0; 

    private SolicitaSuspender solicitaSuspender; // Objeto para gestionar la suspensión.

    // Constructor que inicializa el objeto SolicitaSuspender.
    public HiloSuspender(SolicitaSuspender solicitaSuspender) {
        this.solicitaSuspender = solicitaSuspender;
    }

    // Se detiene el hilo estableciendo la variable `detener` en `true`.
    public void detenerHilo() {
        detener = true;
    }

    // Se suspende el hilo estableciendo la variable `suspendido` en `true`.
    public void suspenderHilo() {
        suspendido = true; // Indica que el hilo debe suspenderse.
        solicitaSuspender.set(true); // Activa la suspensión.
    }

    // Se reanuda el hilo estableciendo la variable `suspendido` en `false`.
    public void reanudarHilo() {
        suspendido = false; // Indica que el hilo debe reanudarse.
        solicitaSuspender.set(false); // Activa la reanudación.
    }

    // Devuelve despçues  el valor actual del contador.
    public int getContador() {
        return contador;
    }

    // Método principal del hilo.
    @Override
    public void run() {
        while (!detener) { 
            contador++; // Se Incrementa el valor del contador.
            System.out.println("Valor del contador: " + contador);

            try {
                Thread.sleep(1000); // La Pausa de 1 segundo.
                solicitaSuspender.esperandoParaReanudar(); // Y después verifica si se debe suspender.
            } catch (InterruptedException e) {
                
                Thread.currentThread().interrupt();
            }
        }
        System.out.println("Hilo finalizado. Valor final del contador: " + contador);
    }
}
