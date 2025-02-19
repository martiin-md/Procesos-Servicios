/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package ExUT2MultiHiloEjercicio3;

/**
 *
 * @author marti
 */
public class SolicitaValor {

    private boolean finImpresion;

    //Hacemos que suspender tenga el valor para después notificarlo
    public synchronized void set(boolean b) {

        finImpresion = b; //Actualiza el estado
        notifyAll(); //Y lo notifica a los hilos para hacerlos en espera
        
    }

    //Pone el hilo en espera si lo suspende es verdadero
    public synchronized void esperaReanundar() throws InterruptedException {

        while (finImpresion) { 
            wait(); 
        }

    }

}
