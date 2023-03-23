# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 10:54:52 2023


@author: Julu

Versión 3.2.5 del Horno. Basada en la v3.1. Esta vez con uso de mi propia
librería art-daq. La cual se descarga a través de pip install art-daq.
También está dentro de una clase, mejorando el estilo de programación para
que no esté todo tirado. Añado funcionalidades para poder trastear sin
necesidad de la tarjeta.


Mejoras TO DO:  
                
                
                
                
Tareas que realiza:     Control de Horno
                        Manejo de los datos
                        Guardar datos
                        Crear un menú de selección.
                        Botón para pausar la adquisición de datos.
                        Elegir si guardar o no los datos.
                        Posibilidad de hacer pruebas con y sin DAQ
"""



import matplotlib.pyplot as plt
import matplotlib.animation as animation
import csv
import tkinter as tk
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from art_daq import prueba


    
class HornoControl:
    
    # Este método se llama cuando se crea una nueva instancia de la clase.
    # Se utiliza para inicializar los atributos de la clase.
    # Básicamente el constructor
    def __init__(self):
        # Inicializa el contador de tiempo, la temperatura global, las listas para las gráficas y los valores máximo y mínimo de temperatura.
        self.count = 0
        self.tempG = 0
        self.x, self.y1, self.y2, self.y3 = [], [], [], []
        self.max_temp = 25
        self.min_temp = 20
        self.paused = False
        
        # Nombre del device
        self.device_name = prueba.get_connected_device()
        if self.device_name is None:
            self.device_name = "Dev1"
        # Canales de entrada y salida del horno.
        self.chan_d = self.device_name+"/port0/line1"
        self.chan_a = self.device_name+"/ao0"

        # Crea la interfaz gráfica de usuario utilizando tkinter.
        self.setup_gui()



     # Este método crea la interfaz gráfica de usuario utilizando tkinter.   
    def setup_gui(self):
        # Crea la ventana principal de la aplicación.
        self.root = tk.Tk()
        # self.root.geometry("1000x600")
        
        # Crea un marco para contener los widgets.
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        
        # Crea una gráfica utilizando matplotlib y la coloca en la parte superior del marco.
        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        # Crea un marco para contener los widgets de temperatura máxima y mínima.
        temp_frame = tk.Frame(self.frame)
        temp_frame.pack(side=tk.TOP, padx=20, pady=20, anchor="center")
        
        # Crea una subventana para los widgets relacionados con la temperatura máxima.
        max_temp_frame = tk.Frame(temp_frame)
        max_temp_frame.pack(side=tk.LEFT)
        
        # Crea una etiqueta para la temperatura máxima y la agrega a la subventana.
        self.max_temp_label = tk.Label(max_temp_frame, text="Temperatura Máxima:")
        self.max_temp_label.pack(side=tk.TOP, padx=20)
        
        # Crea una caja de texto para ingresar la temperatura máxima y la agrega a la subventana.
        self.max_temp_entry = tk.Entry(max_temp_frame)
        self.max_temp_entry.pack(side=tk.TOP)
        
        # Crea un botón para actualizar la temperatura máxima y lo agrega a la subventana.
        self.update_max_temp_button = tk.Button(max_temp_frame, text="Actualizar Máxima", command=self.update_max_temp)
        self.update_max_temp_button.pack(side=tk.TOP, pady=10)
        
        # Crea una subventana para los widgets relacionados con la temperatura mínima.
        min_temp_frame = tk.Frame(temp_frame)
        min_temp_frame.pack(side=tk.LEFT)
        
        # Crea una etiqueta para la temperatura mínima y la agrega a la subventana.
        self.min_temp_label = tk.Label(min_temp_frame, text="Temperatura Mínima:")
        self.min_temp_label.pack(side=tk.TOP, padx=20)
        
        # Crea una caja de texto para ingresar la temperatura mínima y la agrega a la subventana.
        self.min_temp_entry = tk.Entry(min_temp_frame)
        self.min_temp_entry.pack(side=tk.TOP)
        
        # Crea un botón para actualizar la temperatura mínima y lo agrega a la subventana.
        self.update_min_temp_button = tk.Button(min_temp_frame, text="Actualizar Mínima", command=self.update_min_temp)
        self.update_min_temp_button.pack(side=tk.TOP, pady=10)
        
        # Crea un botón para salir de la aplicación y lo agrega a la ventana principal.
        self.exitButton = tk.Button(self.root, text="SALIR", command=self.root.destroy, fg="red")
        self.exitButton.pack(side=tk.BOTTOM, pady=10)
        
        
        # Crea una animación para actualizar la gráfica de temperatura en tiempo real.
        self.ani = animation.FuncAnimation(plt.gcf(), self.grafica_real_time, interval=500)
        self.ani_running = self.canvas.get_tk_widget().after(0, self.ani.event_source.start)
    
        # Crea el botón de guardar los datos
        self.save_button = tk.Button(self.root, text="Guardar datos", command=self.save_data)
        self.save_button.pack(side=tk.BOTTOM, pady=10)   
        
        # Crea el botón de pausa
        self.pause_button = tk.Button(self.root, text="Pausar", command=self.toggle_pause)
        self.pause_button.pack(side=tk.BOTTOM, pady=10)
        
        # Crea una animación para actualizar la gráfica de temperatura en tiempo real.
        self.ani = animation.FuncAnimation(plt.gcf(), self.grafica_real_time, interval=500)
        self.ani_running = self.canvas.get_tk_widget().after(0, self.ani.event_source.start)
    
        
        
    def run(self):
        try:
            # prueba.safe_state(self.device_name)
            self.root.mainloop()
            
        finally:
            # prueba.safe_state(self.device_name)
            # self.exportar_datos_csv(self.x, self.y1, self.y2, self.y3)
            pass



    def exportar_datos_csv(self, x, y1, y2, y3):
        # Crear ventana pop-up
        root = tk.Tk()
        root.withdraw()  
        # Abrir diálogo para seleccionar la ruta y el nombre del archivo
        nombre_archivo = tk.filedialog.asksaveasfilename(defaultextension=".csv")
        
        # Escribir datos en el archivo CSV
        with open(nombre_archivo, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Tiempo (s)", "Temperatura (°C)", "Temp. Máx (°C)", "Temp. Mín (°C)"])
            for i in range(len(x)):
                writer.writerow([x[i], y1[i], y2[i], y3[i]])



    def transform_voltage_temp(self):
        # Cambiar de Voltaje a temperatura
        temp = prueba.get_voltage_analogic(self.device_name+"/ai0")*100 
        # print("Temperatura leída: {:.2f} ºC".format(temp))
        return temp

       
       
    # Este método se encarga de actualizar la gráfica de temperatura en tiempo real.   
    def grafica_real_time(self, i):
        if not self.paused:
            self.pause_button.config(text="Pausar")
            self.count += 1
            
            # Agregar un nuevo valor al eje x de la gráfica
            self.x.append(self.count*0.5)
            self.tempG
            self.max_temp
            self.min_temp
            # Obtener la temperatura actual y agregarla al eje y de la gráfica
            # self.tempG = self.transform_voltage_temp()
            
            # Obtener temperatura pseudorandom
            self.tempG = self.random_number_between_20_and_40(self.tempG)
            self.y1.append(self.tempG)
            self.y2.append(self.max_temp)
            self.y3.append(self.min_temp)
            
            # Imprimir el tiempo transcurrido y la temperatura actual en la consola - Debug option
            print("Tiempo: {:.2f}s, Temperatura {:.2f}".format(self.count*0.5,self.tempG))
            
            # Borrar la gráfica anterior para actualizarla con la nueva información
            plt.cla()
            # Graficar los datos actualizados
            plt.plot(self.x,self.y1,label='Temperatura')
            plt.plot(self.x,self.y2,label='Temp. Máx')
            plt.plot(self.x,self.y3,label='Temp. Mín')
            
            if self.max_temp < self.min_temp:
                self.max_temp = self.min_temp + 2
            
            if self.max_temp < self.tempG:
                print("Estamos calientes")
                self.tempG = self.random_number_between_20_and_40(self.tempG, -0.2)
                # print(prueba.set_voltage_analogic(self.chan_a, 0))
                # prueba.set_voltage_digital(self.chan_d, True)
            
            elif self.tempG < self.min_temp:
                print("Estamos frios")
                self.tempG = self.random_number_between_20_and_40(self.tempG, 0.2)
                # prueba.set_voltage_digital(self.chan_d, False)
                # print(prueba.set_voltage_analogic(self.chan_a, 5))
            else:
                print("tamo bien")
                self.tempG = self.random_number_between_20_and_40(self.tempG)
                # prueba.set_voltage_digital(self.chan_d, False)
                # print(prueba.set_voltage_analogic(self.chan_a, 2.5))
        else:
            self.pause_button.config(text="Reanudar")
               
       
       
    # Este método actualiza la temperatura máxima cuando se pulsa el botón correspondiente.
    def update_max_temp(self):
        # Obtiene la temperatura ingresada por el usuario.
        temp_str = self.max_temp_entry.get()
        # Si se ingresó una temperatura, la convierte en un número flotante y la actualiza.
        if temp_str:
            self.max_temp = float(temp_str)



    # Este método actualiza la temperatura mínima cuando se pulsa el botón correspondiente.
    def update_min_temp(self):
        # Obtiene la temperatura ingresada por el usuario.
        temp_str = self.min_temp_entry.get()
        # Si se ingresó una temperatura, la convierte en un número flotante y la actualiza.
        if temp_str:
            self.min_temp = float(temp_str)
       
    # Este método genera un número pseudoaleatorio entre 20 y 40,
    # con una variación máxima de 0.2 respecto al número anterior.
    # Permite un incremento por parámetro para poder imitar el horno
    # Se usa cuando no se tiene a mano la DAQ
    def random_number_between_20_and_40(self, last_number=None, increment=0):
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

    
    def toggle_pause(self):
        self.paused = not self.paused
        
    def save_data(self):
        self.exportar_datos_csv(self.x, self.y1, self.y2, self.y3)
       
if __name__ == "__main__":
    horno_control = HornoControl()
    horno_control.run()
    
    
    
