/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package ExUT2MultiHiloEjercicio3;

import java.util.Scanner;

/**
 *
 * @author marti
 */
public class Main {

    public static void main(String[] args) {
        SolicitaValor solicitarValor = new SolicitaValor();
        HiloImpresion hilo = new HiloImpresion(solicitarValor);

        hilo.start(); // Se inicia el hilo.

        Scanner scanner = new Scanner(System.in);
        String entrada;

        do {
            System.out.println("Introduce S para suspender R para reanudar o * para finalizar:");
            entrada = scanner.nextLine();

            // Suspende el hilo si el usuario introduce "S".
            if (entrada.equalsIgnoreCase("S")) {
                hilo.suspenderHilo();
            } // Reanuda el hilo si el usuario introduce "R".
            else if (entrada.equalsIgnoreCase("R")) {
                hilo.reanudarHilo();
            }

        } while (!entrada.equals("*")); // Finaliza el bucle si se introduce "*".

        // Detiene el hilo y finaliza el programa.
        hilo.finalizarPrograama();
    }
}


