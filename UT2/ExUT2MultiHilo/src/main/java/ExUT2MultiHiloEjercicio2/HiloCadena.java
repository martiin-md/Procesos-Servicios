/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package ExUT2MultiHiloEjercicio2;


/**
 *
 * @author martin
 */
public class HiloCadena extends Thread {

    private ImprimirCadena imprimirCadena; 
    private String palabra;
    private int miTurno; 
    
    // Constructor que inicializa los atributos del hilo
    public HiloCadena(ImprimirCadena imprimirCadena, String palabra, int miTurno) {
        this.imprimirCadena = imprimirCadena;
        this.palabra = palabra;
        this.miTurno = miTurno;
    }

    // Metodo run que se ejecuta cuando el hilo empieza
    @Override
    public void run() {
        for (int i = 0; i < 5; i++) { // Imprimo la palabra 5 veces
            imprimirCadena.PintaCadena(palabra, miTurno); // Llammao al metodo PintaCadena para imprimir la palabra en el turno correspondiente
        }
    }
}

