/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package ExUT2MultiHiloEjercicio2;

/**
 *
 * @author martin
 */
public class PimPamPumBase1 {

    public static void main(String[] args) {
        ImprimirCadena imprimirCadena = new ImprimirCadena();
        HiloCadena hilo1 = new HiloCadena(imprimirCadena, "PIM", 1);
        HiloCadena hilo2 = new HiloCadena(imprimirCadena, "PAM", 2);
        HiloCadena hilo3 = new HiloCadena(imprimirCadena, "PUM", 3);

        hilo1.start();
        hilo2.start();
        hilo3.start();
    }
}
