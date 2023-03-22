# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 19:03:08 2023

@author: Julu

Versión 2.0 del Horno. Basada en la v1.0. Esta vez con uso de mi propia
librería art-daq. La cual se descarga a través de pip install art-daq.


Mejoras TO DO:  Limpieza de programa
                Colocar de manera más aesthetic los botones
                Guardar datos
                Crear un menú de selección.
                
Tareas que realiza:     Control de Horno
                        Manejo de los datos
                        

"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from art_daq import prueba



def transform_voltage_temp():
    # Cambiar de Voltaje a temperatura
    temp = prueba.get_voltage_analogic("PFG/ai0")*100 
    # print("Temperatura leída: {:.2f} ºC".format(temp))
    return temp



try:            
    prueba.safe_state("PFG")
    chan_d = "PFG/port0/line1"
    chan_a = "PFG/ao0"
    
    # Inicializar las variables "count", "x" e "y"
    count = 0  # Contador del tiempo transcurrido
    tempG = 0
    x, y1, y2, y3 = [], [], [], []  # Listas vacías para almacenar los valores de tiempo y temperatura
    max_temp = 25  # Valor por defecto de la temperatura máxima
    min_temp = 20  # Valor por defecto de la temperatura mínima
    
    def grafica_real_time(i):
        
        global count
        count += 1
        
        # Agregar un nuevo valor al eje x de la gráfica
        x.append(count*0.5)
        global tempG
        global max_temp
        global min_temp
        # Obtener la temperatura actual y agregarla al eje y de la gráfica
        tempG = transform_voltage_temp()
        y1.append(tempG)
        y2.append(max_temp)
        y3.append(min_temp)
        
        # Imprimir el tiempo transcurrido y la temperatura actual en la consola - Debug option
        print("Tiempo: {:.2f}s, Temperatura {:.2f}".format(count*0.5,tempG))
        
        # Borramos la gráfica anterior para actualizarla con la nueva información
        plt.cla()
        # Graficamos los datos actualizados
        plt.plot(x,y1,label='Temperatura')
        plt.plot(x,y2,label='Temp. Máx')
        plt.plot(x,y3,label='Temp. Mín')
        
        if max_temp < min_temp:
            max_temp = min_temp + 2
        
        if max_temp < tempG:
            print("Estamos calientes")
            print(prueba.set_voltage_analogic(chan_a, 0))
            prueba.set_voltage_digital(chan_d, True)

        elif tempG < min_temp:
            print("Estamos frios")
            prueba.set_voltage_digital(chan_d, False)
            print(prueba.set_voltage_analogic(chan_a, 5))
        else:
            print("tamo bien")
            prueba.set_voltage_digital(chan_d, False)
            print(prueba.set_voltage_analogic(chan_a, 2.5))
            
    
    
    def update_max_temp():
        global max_temp
        temp_str = max_temp_entry.get()
        if temp_str:
            max_temp = float(temp_str)
        
    def update_min_temp():
        global min_temp
        temp_str = min_temp_entry.get()
        if temp_str:
            min_temp = float(temp_str)
    
    
    
    # Crear la interfaz gráfica
    root = Tk()
    root.geometry("1000x600")
    
    # Crear el marco
    frame = Frame(root)
    frame.pack()
    
    # Cuadro de entrada para la temperatura máxima
    max_temp_label = Label(frame, text="Temperatura Máxima:")
    max_temp_label.pack(side=LEFT)
    max_temp_entry = Entry(frame)
    max_temp_entry.pack(side=LEFT)
    
    # Cuadro de entrada para la temperatura mínima
    min_temp_label = Label(frame, text="Temperatura Mínima:")
    min_temp_label.pack(side=LEFT)
    min_temp_entry = Entry(frame)
    min_temp_entry.pack(side=LEFT)
    
    
    # Botón para salir de la aplicación
    exitButton = Button(root, text="SALIR", command=root.destroy)
    exitButton.pack(side=BOTTOM)
    
    # Botón para actualizar la temperatura máxima
    update_max_temp_button = Button(root, text="Actualizar Máxima", command=update_max_temp)
    update_max_temp_button.pack(side=BOTTOM)
    
    # Botón para actualizar la temperatura mínima
    update_min_temp_button = Button(root, text="Actualizar Mínima", command=update_min_temp)
    update_min_temp_button.pack(side=BOTTOM)
    

    
    
    # # Crear un widget de cuadro de lienzo en el marco
    canvas = FigureCanvasTkAgg(plt.gcf(), master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=RIGHT, fill=BOTH, expand=1)

    
    
    # Configurar la animación de Matplotlib
    ani = animation.FuncAnimation(plt.gcf(), grafica_real_time, interval=500)

    

    # Agregar la animación al widget de canvas
    ani_running = canvas.get_tk_widget().after(0, ani.event_source.start)
    
    
    # Iniciar el bucle de eventos de la interfaz gráfica
    root.mainloop()

finally:
    prueba.safe_state("PFG")





