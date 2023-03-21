# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 15:53:31 2023

@author: julu

Versión 1.0 del Horno. Basada en la v0.4. Más limpia, ordenada.
Mejoras TO DO:  Limpieza de programa
                Poner todo en el mismo marco tk--
                Colocar de manera más aesthetic los botones
                
Tareas que realiza:     Control de Horno
                        Manejo de los datos
                        
"""

import nidaqmx as daq 
import atexit
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg




def get_voltage_analog_0():
    with daq.Task() as task:
        task.ao_channels.add_ao_voltage_chan("PFG/ao0")
        voltage = task.read_analog_f64()
        return voltage


def get_state_digital_01():
    with daq.Task() as task:
        task.di_channels.add_di_chan("PFG/port0/line1")
        state = task.read_digital_u8()
        return state


def inicio_estado_seguro():
    with daq.Task() as task_out:
       
       
        # Configurar canales de salida
        for i in range(2):
            task_out.ao_channels.add_ao_voltage_chan("PFG/ao{}".format(i))       
       
        # Escribir voltaje cero en los canales de salida
        task_out.write([0, 0])
      
   
def set_voltage_0(voltage):
    with daq.Task() as task:
        task.ao_channels.add_ao_voltage_chan("PFG/ao0") # Especificar la salida analógica AO0 del dispositivo DAQ
        task.write(voltage, auto_start=True) # Establecer el voltaje en AO0



def set_voltage_digital_01(voltage):
    with daq.Task() as task:
        task.do_channels.add_do_chan("PFG/port0/line1") # Especificar la salida digital 0.1 del dispositivo DAQ
        task.write(voltage) # Establecer el voltaje en 0.1


def read_voltage_mean():
    # Crear una tarea de lectura en el dispositivo DAQ "PFG"
    with daq.Task() as task:
        # Configurar el canal analógico de entrada ai0 en el dispositivo DAQ "PFG"
        # Configurado de tal manera que el modo de input sea RSE
        task.ai_channels.add_ai_voltage_chan("PFG/ai0", terminal_config=daq.constants.TerminalConfiguration.RSE)

        # Leer el voltaje actual del canal ai0 10 veces
        voltages = task.read(number_of_samples_per_channel=10)

        # Calcular la media de los valores leídos
        mean_voltage = sum(voltages)/len(voltages)

 
    # Devolver la media de los voltajes medidos
    return mean_voltage

def transform_voltage_temp():
    # Cambiar de Voltaje a temperatura
    temp = read_voltage_mean()*100 
    # print("Temperatura leída: {:.2f} ºC".format(temp))
    return temp


try:            
    inicio_estado_seguro()    
    
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
            set_voltage_digital_01(True)
            set_voltage_0(0)
        elif tempG < min_temp:
            print("Estamos frios")
            set_voltage_digital_01(False)
            set_voltage_0(5)
        else:
            print("tamo bien")
            set_voltage_digital_01(False)
            set_voltage_0(2.5)
            
    
    
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
    set_voltage_0(0)
    set_voltage_digital_01(False)

# print("El voltaje del canal analógico 0 es:", get_voltage_analog_0())
# print("El estado del canal digital 0.1 es:", get_state_digital_01())



