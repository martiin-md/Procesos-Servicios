/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.mycompany.examenut1martinmd;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.Random;

/**
 *
 * @author martin
 */
public class GeneradorAdivinaHijo {

    public static void main(String[] args) throws IOException {
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(System.out));

        Random numeroAleatorio = new Random();
        int numero = numeroAleatorio.nextInt(100);
        
        String input = reader.readLine();
        int numeroAdivinado = Integer.parseInt(input);

        while ((input = reader.readLine()) != null) {

            if (numeroAdivinado > numero) {
                writer.write("Muy alto\n");
            } else if (numeroAdivinado < numero) {
                writer.write("Muy bajo\n");
            } else {
                writer.write("Correcto\n");
                break;
            }
            writer.flush();
        }
    }
}
