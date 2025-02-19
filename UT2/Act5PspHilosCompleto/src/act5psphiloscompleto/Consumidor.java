/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package act5psphiloscompleto;

/**
 *
 * @author martin
 */
public class Consumidor implements Runnable{
    private final SharedQueue sharedQueue;
    private int contador = 0;
    
    public Consumidor(SharedQueue sharedQueue) {
        this.sharedQueue = sharedQueue;
    }

    @Override
    public void run() {
        try {
            while (true) {                
                sharedQueue.remove();
                contador++; 
                Thread.sleep(60); //Simulamos el tiempo de procesamiento ; Cambie el tiempo de 500 a 60 por el que ira igual de rapido  consumiendo elementos
                System.out.println(Thread.currentThread().getName() + " Consumido " + contador + " elementos ");
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

    }
    
    
}
