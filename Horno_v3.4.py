# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 10:54:52 2023


@author: Julu

Versión 3.3 del Horno. Basada en la v3.2.5. Esta vez con uso de mi propia
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


import matplotlib.animation as animation
import csv
import tkinter as tk
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
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
        self.paused = False           # Indicador de si se pausó la adquisición de datos

        # Nombre del device
        self.device_name = daq.get_connected_device()
        if self.device_name is None:
            self.device_name = "Dev1"

        self.horno_daq = HornoDAQ(self.device_name, self)
        self.horno_gui = HornoGUI(self)

        # Crea la interfaz gráfica de usuario utilizando tkinter.
        self.horno_gui.setup_gui()

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

    def exportar_datos_csv(self, x, y1, y2, y3):
        """
        Esta función escribe los datos de la medición en un archivo CSV. Primero,
        abre un diálogo para seleccionar la ruta y el nombre del archivo. Luego,
        escribe los datos en el archivo CSV.

        @param x: una lista con los valores de tiempo.
        @param y1: una lista con los valores de temperatura.
        @param y2: una lista con los valores de temperatura máxima.
        @param y3: una lista con los valores de temperatura mínima.
        """
        # Crear ventana pop-up
        root = tk.Tk()
        root.withdraw()
        # Abrir diálogo para seleccionar la ruta y el nombre del archivo
        nombre_archivo = tk.filedialog.asksaveasfilename(
            defaultextension=".csv")

        # Escribir datos en el archivo CSV
        with open(nombre_archivo, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Tiempo (s)", "Temperatura (°C)",
                            "Temp. Máx (°C)", "Temp. Mín (°C)"])
            for i in range(len(x)):
                writer.writerow([x[i], y1[i], y2[i], y3[i]])

    def random_number_between_20_and_40(self, last_number=None, increment=0):
        """
        Genera un número pseudoaleatorio entre 20 y 40,
        con una variación máxima de 0.2 respecto al número anterior.
        Permite un incremento por parámetro para poder simular
        la temperatura en ausencia de la DAQ.

        @param last_number: el último número generado (opcional).
        @param increment: el valor de incremento a sumar al número generado (opcional).

        @return: el número aleatorio generado, con un máximo de variación de 0.2 respecto al número anterior.
        """

        # Definir el rango de números permitidos
        min_number = 20
        max_number = 40
        # Establecer la diferencia máxima permitida entre el último número generado y el siguiente
        allowed_diff = 0.2

        # Si no se ha generado un número previamente (last_number es None),
        # generar un número aleatorio entre el rango permitido
        if last_number is None:
            return random.uniform(min_number, max_number)

        # Establecer el límite inferior para el próximo número aleatorio,
        # asegurándose de que no sea menor que el mínimo permitido
        min_limit = max(min_number, last_number - allowed_diff)

        # Establecer el límite superior para el próximo número aleatorio,
        # asegurándose de que no sea mayor que el máximo permitido
        max_limit = min(max_number, last_number + allowed_diff)

        # Generar y devolver un número aleatorio entre los límites calculados,
        # sumando el valor del incremento dado por parámetro
        return random.uniform(min_limit, max_limit) + increment

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


class HornoGUI:

    def __init__(self, horno_control):
        self.horno_control = horno_control
        self.HornoDAQ = HornoDAQ(horno_control.device_name, horno_control)
        # self.setup_gui()

    def setup_gui(self):
        """
        Esta función crea la interfaz gráfica de usuario utilizando tkinter.
        """
        # Crea la ventana principal de la aplicación.
        self.horno_control.root = tk.Tk()

        # self.root.geometry("1000x600")

        # Crea un marco para contener los widgets.
        self.horno_control.frame = tk.Frame(self.horno_control.root)
        self.horno_control.frame.pack()

        # Crea una figura y ejes utilizando la interfaz orientada a objetos.
        fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = fig.add_subplot(111)

        # Crea una gráfica utilizando matplotlib y la coloca en la parte superior del marco.
        self.horno_control.canvas = FigureCanvasTkAgg(
            fig, master=self.horno_control.frame)
        self.horno_control.canvas.draw()
        self.horno_control.canvas.get_tk_widget().pack(
            side=tk.TOP, fill=tk.BOTH, expand=1)

        # Crea un marco para contener los widgets de temperatura máxima y mínima.
        temp_frame = tk.Frame(self.horno_control.frame)
        temp_frame.pack(side=tk.TOP, padx=20, pady=20, anchor="center")

        # Crea una subventana para los widgets relacionados con la temperatura máxima.
        max_temp_frame = tk.Frame(temp_frame)
        max_temp_frame.pack(side=tk.LEFT)

        # Crea una etiqueta para la temperatura máxima y la agrega a la subventana.
        self.horno_control.max_temp_label = tk.Label(
            max_temp_frame, text="Temperatura Máxima:")
        self.horno_control.max_temp_label.pack(side=tk.TOP, padx=20)

        # Crea una caja de texto para ingresar la temperatura máxima y la agrega a la subventana.
        self.horno_control.max_temp_entry = tk.Entry(max_temp_frame)
        self.horno_control.max_temp_entry.pack(side=tk.TOP)

        # Crea un botón para actualizar la temperatura máxima y lo agrega a la subventana.
        self.horno_control.update_max_temp_button = tk.Button(
            max_temp_frame, text="Actualizar Máxima", command=self.update_max_temp)
        self.horno_control.update_max_temp_button.pack(side=tk.TOP, pady=10)

        # Crea una subventana para los widgets relacionados con la temperatura mínima.
        min_temp_frame = tk.Frame(temp_frame)
        min_temp_frame.pack(side=tk.LEFT)

        # Crea una etiqueta para la temperatura mínima y la agrega a la subventana.
        self.horno_control.min_temp_label = tk.Label(
            min_temp_frame, text="Temperatura Mínima:")
        self.horno_control.min_temp_label.pack(side=tk.TOP, padx=20)

        # Crea una caja de texto para ingresar la temperatura mínima y la agrega a la subventana.
        self.horno_control.min_temp_entry = tk.Entry(min_temp_frame)
        self.horno_control.min_temp_entry.pack(side=tk.TOP)

        # Crea un botón para actualizar la temperatura mínima y lo agrega a la subventana.
        self.horno_control.update_min_temp_button = tk.Button(
            min_temp_frame, text="Actualizar Mínima", command=self.update_min_temp)
        self.horno_control.update_min_temp_button.pack(side=tk.TOP, pady=10)

        # Crea un botón para salir de la aplicación y lo agrega a la ventana principal.
        self.horno_control.exitButton = tk.Button(
            self.horno_control.root, text="SALIR", command=self.horno_control.root.destroy, fg="red")
        self.horno_control.exitButton.pack(side=tk.BOTTOM, pady=10)

        # Crea una animación para actualizar la gráfica de temperatura en tiempo real.
        self.horno_control.ani = animation.FuncAnimation(
            fig, self.grafica_real_time, interval=500)
        self.horno_control.ani_running = self.horno_control.canvas.get_tk_widget(
        ).after(0, self.horno_control.ani.event_source.start)

        # Crea el botón de guardar los datos
        self.horno_control.save_button = tk.Button(
            self.horno_control.root, text="Guardar datos", command=self.horno_control.save_data)
        self.horno_control.save_button.pack(side=tk.BOTTOM, pady=10)

        # Crea el botón de pausa
        self.horno_control.pause_button = tk.Button(
            self.horno_control.root, text="Pausar", command=self.horno_control.toggle_pause)
        self.horno_control.pause_button.pack(side=tk.BOTTOM, pady=10)

    def grafica_real_time(self, i: int):
        """
        Este método actualiza la gráfica de temperatura en tiempo real.

        @param i: El número de veces que se ha llamado a la función.
        """
        if not self.horno_control.paused:
            self.horno_control.pause_button.config(text="Pausar")
            self.horno_control.count += 1
            self.update_temperature_data()
            self.update_temperature_graph()
            self.check_temperature_range()
        else:
            self.horno_control.pause_button.config(text="Reanudar")

    def update_temperature_data(self):
        self.horno_control.x.append(self.horno_control.count * 0.5)
        self.horno_control.tempG = self.HornoDAQ.transform_voltage_temp()
        self.horno_control.y1.append(self.horno_control.tempG)
        self.horno_control.y2.append(self.horno_control.max_temp)
        self.horno_control.y3.append(self.horno_control.min_temp)
        print("Tiempo: {:.2f}s, Temperatura {:.2f}".format(
            self.horno_control.count * 0.5, self.horno_control.tempG))

    def update_temperature_graph(self):

        self.ax.clear()
        self.ax.plot(self.horno_control.x,
                     self.horno_control.y1, label='Temperatura')
        self.ax.plot(self.horno_control.x,
                     self.horno_control.y2, label='Temp. Máx')
        self.ax.plot(self.horno_control.x,
                     self.horno_control.y3, label='Temp. Mín')

        self.ax.legend(loc='best')
        self.ax.set_xlabel('Tiempo (s)')
        self.ax.set_ylabel('Temperatura (°C)')

    def check_temperature_range(self):
        if self.horno_control.max_temp < self.horno_control.tempG:
            print("Estamos calientes")
            self.HornoDAQ.warm_state()

        elif self.horno_control.tempG < self.horno_control.min_temp:
            print("Estamos frios")
            self.HornoDAQ.cold_state()

        else:
            print("tamo bien")
            self.HornoDAQ.mild_state()

    def update_max_temp(self):
        """
        Este método se encarga de actualizar la temperatura máxima
        cuando se pulsa el botón correspondiente. 
        Obtiene la temperatura ingresada por el usuario
        y la convierte en un número flotante. 
        Luego actualiza la variable de instancia "max_temp" con el nuevo valor.
        """
        try:
            temp_str = self.horno_control.max_temp_entry.get()
            if temp_str:
                temp = float(temp_str)
                self.horno_control.max_temp = temp
        except ValueError:
            tk.messagebox.showerror("Error", "Por favor, ingrese un número válido para la temperatura máxima")


    def update_min_temp(self):
        """
        Este método se encarga de actualizar la temperatura mínima
        cuando se pulsa el botón correspondiente.
        Obtiene la temperatura ingresada por el usuario
        y la convierte en un número flotante.
        Luego actualiza la variable de instancia "min_temp" con el nuevo valor.
        """
        try:
             temp_str = self.horno_control.min_temp_entry.get()
             if temp_str:
                 temp = float(temp_str)
                 self.horno_control.min_temp = temp
        except ValueError:
             tk.messagebox.showerror("Error", "Por favor, ingrese un número válido para la temperatura mínima")

          
class HornoDAQ:
    def __init__(self, device_name, horno_control):
        self.device_name = device_name
        self.chan_d = self.device_name + "/port0/line1"
        self.chan_a = self.device_name + "/ao0"
        self.horno_control = horno_control

    def warm_state(self):
        """Este método establece la salida analógica en 0V
        y la salida digital en HIGH (5V) 
        """
        print(daq.set_voltage_analogic(self.chan_a, 0))
        daq.set_voltage_digital(self.chan_d, True)

    def cold_state(self):
        """Este método establece la salida analógica en 5V
        y la salida digital en LOW (0V) 
        """
        daq.set_voltage_digital(self.chan_d, False)
        print(daq.set_voltage_analogic(self.chan_a, 5))

    def mild_state(self):
        """Este método establece la salida analógica en 2.5V
        y la salida digital en LOW (0V) 
        """
        daq.set_voltage_digital(self.chan_d, False)
        print(daq.set_voltage_analogic(self.chan_a, 2.5))

    def transform_voltage_temp(self):
        """
        Esta función convierte la lectura de voltaje del canal analógico AI0
        en una lectura de temperatura en grados Celsius.
        La función multiplica la lectura de voltaje por 100
        y devuelve el valor de temperatura resultante.

        @return: el valor de la temperatura en grados Celsius.
        """
        # Cambiar de Voltaje a temperatura
        temp = daq.get_voltage_analogic(self.device_name+"/ai0")*100
        # print("Temperatura leída: {:.2f} ºC".format(temp))
        return temp


if __name__ == "__main__":
    horno_control = HornoControl()
    horno_control.run()
