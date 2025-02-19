/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package act5psphiloscompleto;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;

/**
 *
 * @author martin
 */
public class SharedQueue {
//  private final Queue<Integer> queue =  new LinkedList<>();
    private final List<Integer> queue = new ArrayList<>(); // Cambio el LinkedList por el ArrayLis para tener la estructura m�s dinamica
    private final int limit;

    private int contadorProducer = 0;   // Contador para los elementos producidos
    private int contadorConsumidor = 0; // Contador para los elementos consumidos

    public SharedQueue(int limit) {
        this.limit = limit;
    }

    // M�todo para agregar elementos del producer
    public synchronized void add(int value) throws InterruptedException {
        while (queue.size() == limit) {
            wait(); // Hacemos un wait para esperar si la cola est� llena
        }
        queue.add(value); // A�adimos  el valor al final del ArrayList
        contadorProducer++; // Usamos el contador del procucer para aumentar la producci�n
        System.out.println(Thread.currentThread().getName() + " produjo: " + value);
        System.out.println(" Total elementos producidos: " + contadorProducer); //Muestri un mensaje para ver la cantidad de elementos producidos
        notifyAll(); // Hacemos un notifyAll para notificar a los consumidores
    }

    // M�todo para eliminar elementos del consumidor
    public synchronized int remove() throws InterruptedException {
        while (queue.isEmpty()) {
            wait(); // Hacemos el uso tambi�n de wait para esperamos si la cola est� vac�a
        }
        int value = queue.remove(0); // Eliminar el primer elemento del ArrayList (FIFO)
        contadorConsumidor++; // Aumentamos el valor de elementos del contador
        System.out.println(Thread.currentThread().getName() + " consumi�: " + value);
        System.out.println(" Total elementos consumidos: " + contadorConsumidor); //Mostramos un mensaje para ver la cantidad de elementos consumidos
        notifyAll(); // Notificamos a los productores
        return value;
    }
}
