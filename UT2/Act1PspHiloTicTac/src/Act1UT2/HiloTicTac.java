package Act1UT2;

/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */

/**
 *
 * @author martin
 */
public class HiloTicTac {
    public static void main(String[] args) {
        Clase hiloTic = new Clase("TIC", 1000);
        Clase hiloTac = new Clase("TAC", 1000);
        
        hiloTic.start();
        hiloTac.start();
    }
}
