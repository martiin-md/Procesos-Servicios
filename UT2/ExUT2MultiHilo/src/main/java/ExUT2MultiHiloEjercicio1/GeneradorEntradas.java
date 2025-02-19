package ExUT2MultiHiloEjercicio1;

import java.util.Random;

/**
 *
 * @author martin
 */
public class GeneradorEntradas extends Thread {

    private Cola colaEntradas;
    private Entrada[] entradasGeneradas;

    public GeneradorEntradas(Cola colaEntradas) {
        this.colaEntradas = colaEntradas;
        this.entradasGeneradas = new Entrada[5]; // Inicializa el array con el tamaño adecuado
    }

    private boolean estaGenerada(int fila, int butaca) {
        for (Entrada entrada : entradasGeneradas) {
            if (entrada != null && entrada.getFila() == fila && entrada.getButaca() == butaca) {
                return true;
            }
        }
        return false;
    }

    /* Utiliza los métodos de la clase para generar las 5 entradas aleatoriamente */
    public void run() {
        Random random = new Random();
        int contador = 0;
        while (contador < 5) {
            int fila = random.nextInt(10) + 1;
            int butaca = random.nextInt(20) + 1;

            if (!estaGenerada(fila, butaca)) {
                Entrada nuevaEntrada = new Entrada(fila, butaca);
                entradasGeneradas[contador] = nuevaEntrada;
                colaEntradas.PutEntrada(nuevaEntrada);
                contador++;
            }
        }
        colaEntradas.setGeneracionTerminada();
    }
}
