/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Main.java to edit this template
 */
package act4pspsuspenderfile;

/**
 *
 * @author martin
 */
public class Act4PspSuspenderFile {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) throws InterruptedException {

        Hilo hilo = new Hilo();
        hilo.suspenderHilo();

        Thread.sleep(5000);
        System.out.println("Suspendiendo el hilo...");
        hilo.suspenderHilo();

        Thread.sleep(5000);
        System.out.println("Reanudando el hilo...");
        hilo.reanudarHilo();
    }
}
