/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package ExUT2MultiHiloEjercicio1;

/**
 *
 * @author martin
 */
public class Cola {

    private Entrada[] sala; // Array que almacena las entradas
    private int tamano; 
    private int inicio; 
    private int fin; 
    private boolean generacionTerminada = false; // Indica si la generación de entradas ha terminado

    // Método para marcar que la generación de entradas ha terminado
    public void setGeneracionTerminada() {
        generacionTerminada = true;
    }

    // Constructor que inicializa la cola con una capacidad específica
    public Cola(int capacidad) {
        sala = new Entrada[capacidad];
        tamano = 0;
        inicio = 0;
        fin = 0;
    }

    // Método para poner una entrada en la cola
    public void PutEntrada(Entrada entrada) {
        sala[fin] = entrada; 
        fin = (fin + 1) % sala.length; 
        tamano++; 
    }

    // Método para obtener una entrada de la cola
    public Entrada getEntrada() {
        while (tamano <= 0) {
            if (generacionTerminada) {
                return null; 
            }
        }
        Entrada entrada = sala[inicio]; 
        inicio = (inicio + 1) % sala.length; 
        tamano--; // Decrementa el tamaño de la cola
        return entrada; // y devuelve después la entrada obtenida
    }

    // Método para verificar si la cola está vacía
    public boolean isEmpty() {
        return tamano == 0; // devuelve true si el tamaño de la cola es 0
    }
}
