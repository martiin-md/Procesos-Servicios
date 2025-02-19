/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Main.java to edit this template
 */
package act5psphiloscompleto;

/**
 *
 * @author martin
 */
public class Main {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        //Creamos la cola compartida
       SharedQueue sharedQueue = new SharedQueue(5); 

       // Crear productores y consumidores
       Thread producer1 = new Thread(new Producer(sharedQueue), " Productor 1 "); 
       Thread producer2 = new Thread(new Producer(sharedQueue), " Productor 2 "); 
       Thread producer3 = new Thread(new Producer(sharedQueue), " Productor 3 "); 
       Thread producer4 = new Thread(new Producer(sharedQueue), " Productor 4 "); 
       Thread producer5 = new Thread(new Producer(sharedQueue), " Productor 5 "); 
       Thread consumer1 = new Thread(new Consumidor(sharedQueue), " Consumidor 1 "); 
       Thread consumer2 = new Thread(new Consumidor(sharedQueue), " Consumidor 2 ");
       
       //Iniciamos los Hilos
       producer1.start(); 
       producer2.start(); 
       producer3.start(); 
       producer4.start(); 
       producer5.start(); 
       consumer1.start(); 
       consumer2.start();

    }
    
}
