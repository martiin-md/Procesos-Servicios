/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package act5psphiloscompleto;

/**
 *
 * @author martin
 */
public class Producer implements Runnable {

    private final SharedQueue sharedQueue;
    private int contador = 0; //Contador para contar la produccion
    
    public Producer(SharedQueue sharedQueue) {
        this.sharedQueue = sharedQueue;
    }

    @Override
    public void run() {

        try {
            while (true) {
                int value = (int) (Math.random() * 100); // Generamos un número aleatorio
                contador++;
                sharedQueue.add(value);
                System.out.println(Thread.currentThread().getName() + " Producido " + contador + " elementos ");
                Thread.sleep(60); //Simulamos el tiempo de producción ; Cambie el tiempo de 1000 a 60 por el que ira más rápido produciendo

            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

    }
}
