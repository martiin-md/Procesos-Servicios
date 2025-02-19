/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.mycompany.examenut1martinmd;

import java.io.BufferedReader;
import java.io.InputStreamReader;

import java.io.*;

/**
 *
 * @author martin
 */
public class JuegoAdivinaPadre {

    public static void main(String[] args) throws IOException, InterruptedException {
        ProcessBuilder pb = new ProcessBuilder("java", "GeneradorAdivinaHijo.java");
        Process procesoHijo = pb.start();

        BufferedReader reader = new BufferedReader(new InputStreamReader(procesoHijo.getInputStream()));
        BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(procesoHijo.getOutputStream()));
        BufferedReader teclado = new BufferedReader(new InputStreamReader(System.in));

        String  pista;
        while (true) {
            System.out.print("Juego Adivinar El Número del 0 al 100 ");
            String numero = teclado.readLine();
            writer.write(numero + "\n");
            writer.flush();

            pista = reader.readLine();
            System.out.println("Pista: " + pista);

            if ("Correcto".equals(pista)) {
                break;
            }
        }

        procesoHijo.waitFor();
        System.out.println("EL JUEGO A ACABDO.....");
    }

}
