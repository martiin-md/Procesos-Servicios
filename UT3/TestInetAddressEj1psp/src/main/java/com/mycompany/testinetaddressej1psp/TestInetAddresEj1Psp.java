/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.mycompany.testinetaddressej1psp;

import java.net.InetAddress;
import java.net.UnknownHostException;

/**
 *
 * @author martin
 */
public class TestInetAddresEj1Psp {
    public static void main(String[] args) {
        // Prueba con localhost
        System.out.println("=====================");
        System.out.println("SALIDA PARA LOCALHOST");
        mostrarInformacion("localhost");

        // Prueba con una URL
        System.out.println("=====================");
        System.out.println("SALIDA PARA UNA URL");
        mostrarInformacion("www.educamosclm.castillalamancha.es");

        // Prueba con el nombre de la máquina local
        System.out.println("=====================");
        System.out.println("SALIDA PARA EL NOMBRE DE LA MÁQUINA");
        try {
            String localHostName = InetAddress.getLocalHost().getHostName();
            mostrarInformacion(localHostName);
        } catch (UnknownHostException e) {
            System.err.println("Error obteniendo el nombre de la máquina local: " + e.getMessage());
        }

        // Prueba con todas las direcciones IP de un dominio
        System.out.println("=====================");
        System.out.println("DIRECCIONES IP PARA: www.google.es");
        mostrarTodasLasDirecciones("www.google.es");
        System.out.println("=====================");
    }

    /**
     * Muestra información sobre un host dado (puede ser un nombre, URL o IP).
     * 
     * @param host El nombre del host, URL o dirección IP.
     */
    private static void mostrarInformacion(String host) {
        try {
            InetAddress dir = InetAddress.getByName(host);
            pruebaMetodos(dir);
        } catch (UnknownHostException e) {
            System.err.println("Error obteniendo información para " + host + ": " + e.getMessage());
        }
    }

    /**
     * Muestra todas las direcciones IP asociadas con un dominio.
     * 
     * @param dominio El nombre del dominio.
     */
    private static void mostrarTodasLasDirecciones(String dominio) {
        try {
            InetAddress[] direcciones = InetAddress.getAllByName(dominio);
            for (InetAddress direccion : direcciones) {
                System.out.println("\t" + direccion);
            }
        } catch (UnknownHostException e) {
            System.err.println("Error obteniendo direcciones IP para " + dominio + ": " + e.getMessage());
        }
    }

    /**
     * Imprime la información proporcionada por los métodos de InetAddress.
     * 
     * @param dir La dirección InetAddress de la que se quiere mostrar información.
     */
    private static void pruebaMetodos(InetAddress dir) {
        System.out.println("\tMetodo getHostName(): " + dir.getHostName());
        System.out.println("\tMetodo getHostAddress(): " + dir.getHostAddress());
        System.out.println("\tMetodo toString(): " + dir.toString());
        System.out.println("\tMetodo getCanonicalHostName(): " + dir.getCanonicalHostName());
    }
}
