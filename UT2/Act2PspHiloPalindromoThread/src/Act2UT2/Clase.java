/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package Act2UT2;

/**
 *
 * @author martin
 */
public class Clase extends Thread {

    String palabra;

    public Clase(String palabra) {
        this.palabra = palabra;
    }

    public boolean charAT(String palabra) {
        int longitud = palabra.length();
        for (int i = 0; i < longitud / 2; i++) {
            if (palabra.charAt(i) != palabra.charAt(longitud - i - 1)) {
                return false;
            }
        }
        return true;
    }

    @Override
    public void run() {
        if (charAT(palabra)) {
            System.out.println("Palabra" + palabra + "Es Palindromo");
        } else {
            System.out.println("Palabra" + palabra + "No es Palindromo");

        }
    }

}
