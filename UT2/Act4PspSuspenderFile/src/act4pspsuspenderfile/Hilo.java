/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package act4pspsuspenderfile;

/**
 *
 * @author martin
 */
public class Hilo {

    private SolicitaSuspender suspender = new SolicitaSuspender();

    public void run() {
        try {
            while (true) {
                suspender.esperandoParaReanudar();
                System.out.println("Hilo ejecutándose...");
                Thread.sleep(1000); 
            }
        } catch (InterruptedException e) {
            System.out.println("Hilo interrumpido.");
        }
    }

    public void suspenderHilo() {
        suspender.set(true); 
    }

    public void reanudarHilo() {
        suspender.set(false);
    }
}
