# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 10:54:52 2023


@author: Julu

Versión 3.2 del Horno. Basada en la v3.1. Esta vez con uso de mi propia
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
from tkinter import *
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from art_daq import prueba


    
class HornoControl:
    
    # Este método se llama cuando se crea una nueva instancia de la clase.
    # Se utiliza para inicializar los atributos de la clase.
    def __init__(self):
        # Inicializa el contador de tiempo, la temperatura global, las listas para las gráficas y los valores máximo y mínimo de temperatura.
        self.count = 0
        self.tempG = 0
        self.x, self.y1, self.y2, self.y3 = [], [], [], []
        self.max_temp = 25
        self.min_temp = 20
        self.paused = False
        
        # Nombre del device
        self.device_name = "Dev1"
        # Canales de entrada y salida del horno.
        self.chan_d = self.device_name+"/port0/line1"
        self.chan_a = self.device_name+"/ao0"

        # Crea la interfaz gráfica de usuario utilizando tkinter.
        self.setup_gui()



     # Este método crea la interfaz gráfica de usuario utilizando tkinter.   
    def setup_gui(self):
        # Crea la ventana principal de la aplicación.
        self.root = Tk()
        # self.root.geometry("1000x600")
        
        # Crea un marco para contener los widgets.
        self.frame = Frame(self.root)
        self.frame.pack()
        
        # Crea una gráfica utilizando matplotlib y la coloca en la parte superior del marco.
        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        
        # Crea un marco para contener los widgets de temperatura máxima y mínima.
        temp_frame = Frame(self.frame)
        temp_frame.pack(side=TOP, padx=20, pady=20, anchor="center")
        
        # Crea una subventana para los widgets relacionados con la temperatura máxima.
        max_temp_frame = Frame(temp_frame)
        max_temp_frame.pack(side=LEFT)
        
        # Crea una etiqueta para la temperatura máxima y la agrega a la subventana.
        self.max_temp_label = Label(max_temp_frame, text="Temperatura Máxima:")
        self.max_temp_label.pack(side=TOP, padx=20)
        
        # Crea una caja de texto para ingresar la temperatura máxima y la agrega a la subventana.
        self.max_temp_entry = Entry(max_temp_frame)
        self.max_temp_entry.pack(side=TOP)
        
        # Crea un botón para actualizar la temperatura máxima y lo agrega a la subventana.
        self.update_max_temp_button = Button(max_temp_frame, text="Actualizar Máxima", command=self.update_max_temp)
        self.update_max_temp_button.pack(side=TOP, pady=10)
        
        # Crea una subventana para los widgets relacionados con la temperatura mínima.
        min_temp_frame = Frame(temp_frame)
        min_temp_frame.pack(side=LEFT)
        
        # Crea una etiqueta para la temperatura mínima y la agrega a la subventana.
        self.min_temp_label = Label(min_temp_frame, text="Temperatura Mínima:")
        self.min_temp_label.pack(side=TOP, padx=20)
        
        # Crea una caja de texto para ingresar la temperatura mínima y la agrega a la subventana.
        self.min_temp_entry = Entry(min_temp_frame)
        self.min_temp_entry.pack(side=TOP)
        
        # Crea un botón para actualizar la temperatura mínima y lo agrega a la subventana.
        self.update_min_temp_button = Button(min_temp_frame, text="Actualizar Mínima", command=self.update_min_temp)
        self.update_min_temp_button.pack(side=TOP, pady=10)
        
        # Crea un botón para salir de la aplicación y lo agrega a la ventana principal.
        self.exitButton = Button(self.root, text="SALIR", command=self.root.destroy, fg="red")
        self.exitButton.pack(side=BOTTOM, pady=10)
        
        # Crea una animación para actualizar la gráfica de temperatura en tiempo real.
        self.ani = animation.FuncAnimation(plt.gcf(), self.grafica_real_time, interval=500)
        self.ani_running = self.canvas.get_tk_widget().after(0, self.ani.event_source.start)
    
        # Crea el botón de guardar los datos
        self.save_button = Button(self.root, text="Guardar datos", command=self.save_data)
        self.save_button.pack(side=BOTTOM, pady=10)   
        
        # Crea el botón de pausa
        self.pause_button = Button(self.root, text="Pausar", command=self.toggle_pause)
        self.pause_button.pack(side=BOTTOM, pady=10)
        

        
        
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
        nombre_archivo = filedialog.asksaveasfilename(defaultextension=".csv")
        
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



    def leer_datos_csv(self, nombre_archivo):
       # Leer datos del archivo CSV
       with open(nombre_archivo, 'r') as file:
           reader = csv.reader(file)
           header = next(reader)
           data = list(reader)
       
       # Convertir datos a listas
       tiempo = [float(row[0]) for row in data]
       temperatura = [float(row[1]) for row in data]
       temp_max = [float(row[2]) for row in data]
       temp_min = [float(row[3]) for row in data]

       # Crear gráfica
       plt.plot(tiempo, temperatura, label="Temperatura")
       plt.plot(tiempo, temp_max, label="Temp. Máx")
       plt.plot(tiempo, temp_min, label="Temp. Mín")
       plt.xlabel("Tiempo (s)")
       plt.ylabel("Temperatura (°C)")
       plt.legend()
       plt.show()
       
       
    # Este método se encarga de actualizar la gráfica de temperatura en tiempo real.   
    def grafica_real_time(self, i):
       if not self.paused:
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
                # print(prueba.set_voltage_analogic(self.chan_a, 0))
                # prueba.set_voltage_digital(self.chan_d, True)
            
            elif self.tempG < self.min_temp:
                print("Estamos frios")
                # prueba.set_voltage_digital(self.chan_d, False)
                # print(prueba.set_voltage_analogic(self.chan_a, 5))
            else:
                print("tamo bien")
                # prueba.set_voltage_digital(self.chan_d, False)
                # print(prueba.set_voltage_analogic(self.chan_a, 2.5))
               
       
       
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
       
    def random_number_between_20_and_40(self, previous_number=None):
        if previous_number is None:
            return random.uniform(20, 40)
    
        min_value = max(20, previous_number - 0.2)
        max_value = min(40, previous_number + 0.2)
        return random.uniform(min_value, max_value)
    
    def toggle_pause(self):
        self.paused = not self.paused
        
    def save_data(self):
        self.exportar_datos_csv(self.x, self.y1, self.y2, self.y3)
       
if __name__ == "__main__":
    horno_control = HornoControl()
    horno_control.run()
    
    
    
