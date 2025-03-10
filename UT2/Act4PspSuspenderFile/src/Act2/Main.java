/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package Act2;

import java.util.Scanner;

/**
 *
 * @author martin
 */
public class Main {

    public static void main(String[] args) {
        SolicitaSuspender solicitadorSuspension = new SolicitaSuspender();
        HiloSuspender miHilo = new HiloSuspender(solicitadorSuspension);

        miHilo.start(); // Se inicia el hilo.

        Scanner scanner = new Scanner(System.in);
        String entrada; 

        do {
            System.out.println("Introduce S para suspender, R para reanudar, o * para finalizar:");
            entrada = scanner.nextLine(); 

            // Suspende el hilo si el usuario introduce "S".
            if (entrada.equalsIgnoreCase("S")) {
                miHilo.suspenderHilo();
            } // Reanuda el hilo si el usuario introduce "R".
            else if (entrada.equalsIgnoreCase("R")) {
                miHilo.reanudarHilo();
            }

        } while (!entrada.equals("*")); // Finaliza el bucle si se introduce "*".

        // Detiene el hilo y finaliza el programa.
        miHilo.detenerHilo();
    }
}
