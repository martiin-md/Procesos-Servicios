package Act1UT2;

import java.util.logging.Level;
import java.util.logging.Logger;

/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
/**
 *
 * @author martin
 */
public class Clase extends Thread {

    String palabra;
    int tiempo;

    public Clase(String palabra, int tiempo) {
        this.palabra = palabra;
        this.tiempo = tiempo;
    }

    @Override
    public void run() {

        while (true) {
            System.out.println(palabra);
            try {
                Thread.sleep(tiempo);
            } catch (InterruptedException ex) {
                Logger.getLogger(Clase.class.getName()).log(Level.SEVERE, null, ex);
            }
        }

    }

}
