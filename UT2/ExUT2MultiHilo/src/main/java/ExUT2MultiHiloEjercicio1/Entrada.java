/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package ExUT2MultiHiloEjercicio1;

/**
 *
 * @author martin
 */
public class Entrada {

    //Las Variables
    private int fila;
    private int butaca;
    private boolean disponible;

    //Contructor con todos los cambios
    public Entrada(int fila, int butaca) {
        this.fila = fila;
        this.butaca = butaca;
        this.disponible = true;
    }

    //y los getter y setters
    public int getFila() {
        return fila;
    }

    public int getButaca() {
        return butaca;
    }

    public boolean isDisponible() {
        return disponible;
    }

    public void setDisponible(boolean disponible) {
        this.disponible = disponible;
    }

    //Metodo toString
    public String toString() {
        return "Entrada [fila=" + fila + ", butaca=" + butaca + "]";
    }
}
