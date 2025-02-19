/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package Act2UT2;

/**
 *
 * @author martin
 */
public class PalindromoThread {

    public static void main(String[] args) {

        Clase hilo1 = new Clase(" Martin ");
        Clase hilo2 = new Clase(" java ");

        hilo1.start();
        hilo2.start();
    }
}
