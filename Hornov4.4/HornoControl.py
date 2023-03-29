# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 10:54:52 2023


@author: Julu

Versión 4.4 del Horno. Basada en la v3.5. Esta vez con uso de mi propia
librería art-daq. La cual se descarga a través de pip install art-daq.
También está dentro de una clase, mejorando el estilo de programación para
que no esté todo tirado. Añado funcionalidades para poder trastear sin
necesidad de la tarjeta. Mejora de comentarios, para que tenga el estilo
correcto. 


Mejoras TO DO:          -Parece ser que los comentarios que he hecho hasta   
                        ahora están mal porque no siguen el estilo docstrings
                        y siguen el de javadoc. Cambiar eso cuando tenga tiempo
                        
                
                
                
                
Tareas que realiza:     Control de Horno
                        Manejo de los datos
                        Guardar datos
                        Crear un menú de selección.
                        Botón para pausar la adquisición de datos.
                        Elegir si guardar o no los datos.
                        Posibilidad de hacer pruebas con y sin DAQ
                        Mejores comentarios
"""



from HornoGUI import HornoGUI
from HornoDAQ import HornoDAQ
from art_daq import daq


class HornoControl:

    def __init__(self):
        """
        Constructor de la clase HornoControl.
        Se utiliza para inicializar los atributos de la clase.
        """

        self.count = 0                # Contador de tiempo
        self.tempG = 0                # Temperatura global
        # Listas para graficar los datos
        self.x, self.y1, self.y2, self.y3 = [], [], [], []
        self.max_temp = 25            # Temperatura máxima permitida
        self.min_temp = 20            # Temperatura mínima permitida
        self.paused = True           # Indicador de si se pausó la adquisición de datos
        self.started = False        # Indicador de si se ha iniciado la adquisición de datos

        # Nombre del device
        self.device_name = daq.get_connected_device()
        if self.device_name is None:
            self.device_name = "Dev1"

        self.horno_daq = HornoDAQ(self.device_name, self)
        self.horno_gui = HornoGUI(self, self.horno_daq)

        # Crea la interfaz gráfica de usuario utilizando tkinter.
        # self.horno_gui.setup_gui()

    def run(self):
        """
        Esta función nicia la ejecución del programa y muestra
        la interfaz gráfica de usuario.
        """
        try:
            daq.safe_state(self.device_name)
            self.root.mainloop()

        finally:
            daq.safe_state(self.device_name)
            # self.exportar_datos_csv(self.x, self.y1, self.y2, self.y3)
            pass

    def save_data(self):
        """Este método llama a la función exportar_datos_csv()
        y le pasa los valores de las listas x, y1, y2 y y3 como argumentos
        """
        self.exportar_datos_csv(self.x, self.y1, self.y2, self.y3)

    def toggle_pause(self):
        """Este método cambia el valor de la variable booleana
        self.paused de True a False (y viceversa)
        """
        self.paused = not self.paused


    def toggle_start(self):
        """Este método cambia el valor de la variable booleana
        self.start de True a False (y viceversa)
        """
        self.started = not self.started

if __name__ == "__main__":
    horno_control = HornoControl()
    horno_control.run()
