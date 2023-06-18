# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 20:34:57 2023

@author: Julu


v6.0

Tengo que cambiar la funcion de la temp. Hacer que sea solo del volt*100
Hacer funcion de adquirir voltaje. ¿Cambiar desde ahi? ¿Una func para cada
fuente? ¿Un nuevo HornoOsci-HornoMulti?
También tengo que revisar las dependencias, he metido bastantes nuevas, la
mayoría son librerías de python, pero debo comprobar anyways. 

Voy a tener que meter hilos que comprueben conexiones.

"""

import csv
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import threading
import time
import matplotlib.animation as animation
from art_daq import daq
from Instrumentos import Instrumentos 
import HornoOsciloscopio
import HornoMultimetro
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import ttk


class HornoGUI:
    
    
    def __init__(self, horno_control, horno_daq):
        """
        Inicializa la clase HornoControlUI.
        
        Args:
            horno_control (HornoControl): Instancia de la clase HornoControl.
            horno_daq (HornoDAQ): Instancia de la clase HornoDAQ.
        """
        self.instrumento = Instrumentos.DAQ #Inicializo en el DAQ
        self.horno_control = horno_control
        self.horno_daq = horno_daq
        self.__init_ui__()
    
    def __init_ui__(self):
        """
        Crea la interfaz gráfica de usuario utilizando tkinter y ttk.
        """
        self.create_main_window()
        self.create_temperature_graph()
        # self.create_temperature_frame()
        # self.create_button_subframe()
        self.create_subframe_gen()
        
       

    def create_main_window(self):
        # Crea la ventana principal de la aplicación.
        self.horno_control.root = tk.Tk()
        # self.horno_control.root.resizable(0, 0)
        # Crea un marco para contener los widgets.
        self.horno_control.frame = ttk.Frame(self.horno_control.root)
        self.horno_control.frame.grid(row=0, column=0, sticky=(tk.W+tk.E+tk.N+tk.S))
        # Expansion
        self.horno_control.root.rowconfigure(1, weight=1)
        self.horno_control.root.columnconfigure(1, weight=1)
        
        # Additional configuration for child widgets
        self.horno_control.frame.rowconfigure(0, weight=1)
        self.horno_control.frame.columnconfigure(0, weight=1)
        

        # self.horno_control.frame.pack()
        
        
    def create_temperature_graph(self):
        # Crea una figura y ejes utilizando la interfaz orientada a objetos.
        fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = fig.add_subplot(111)
        
        # Crea una gráfica utilizando matplotlib y la coloca en la parte superior del marco.
        self.horno_control.canvas = FigureCanvasTkAgg(fig, master=self.horno_control.frame)
        self.horno_control.canvas.draw()
        self.horno_control.canvas.get_tk_widget().grid(row=0, column=0, padx=0, pady=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        # Escalable
        self.horno_control.root.rowconfigure(0, weight=5)
        self.horno_control.root.columnconfigure(0, weight=5)
        self.create_animation(fig)
        
    def create_temperature_frame(self):
        # Crea un marco para contener los widgets de temperatura máxima y mínima.
        temp_frame = tk.Frame(self.subframe, bg='lightgray')
        temp_frame.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N)
        
        temp_frame.rowconfigure(0, weight=0)
        temp_frame.columnconfigure(0, weight=0)
        
        # Crea una etiqueta para la temperatura actual y la agrega al marco.
        self.horno_control.current_temp_label = tk.Label(temp_frame, text="Temperatura Actual:", font=("Arial", 14), bg='lightgray')
        self.horno_control.current_temp_label.pack(side=tk.TOP, padx=20)
        
        # Crea una etiqueta de solo lectura para mostrar la temperatura actual.
        self.horno_control.current_temp_var = tk.StringVar()
        self.horno_control.current_temp_entry = ttk.Entry(temp_frame, textvariable=self.horno_control.current_temp_var, state="readonly", width=10)
        self.horno_control.current_temp_entry.pack(side=tk.TOP)

        # Crea una subventana para los widgets relacionados con la temperatura mínima.
        min_temp_frame = tk.Frame(temp_frame, bg='lightgray')
        min_temp_frame.pack(side=tk.LEFT)

        # Crea una subventana para los widgets relacionados con la temperatura máxima.
        max_temp_frame = tk.Frame(temp_frame, bg='lightgray')
        max_temp_frame.pack(side=tk.LEFT)
        
        # Crea una etiqueta para la temperatura máxima y la agrega a la subventana.
        self.horno_control.max_temp_label = tk.Label(max_temp_frame, text="Temperatura Máxima:", font=("Arial", 14), bg='lightgray')
        self.horno_control.max_temp_label.pack(side=tk.TOP, padx=20)

        # Crea una caja de texto para ingresar la temperatura máxima y la agrega a la subventana.
        self.horno_control.max_temp_entry = ttk.Entry(max_temp_frame)
        self.horno_control.max_temp_entry.insert(0, self.horno_control.max_temp)
        self.horno_control.max_temp_entry.pack(side=tk.TOP)

        # Crea un botón para actualizar la temperatura máxima y lo agrega a la subventana.
        self.horno_control.update_max_temp_button = ttk.Button(
            max_temp_frame, text="Actualizar Máxima", command=self.update_max_temp)
        self.horno_control.update_max_temp_button.pack(side=tk.TOP, pady=10)
        
        # Crea una etiqueta para la temperatura mínima y la agrega a la subventana.
        self.horno_control.min_temp_label = tk.Label(min_temp_frame, text="Temperatura Mínima:", font=("Arial", 14), bg='lightgray')
        self.horno_control.min_temp_label.pack(side=tk.TOP, padx=20)

        # Crea una caja de texto para ingresar la temperatura mínima y la agrega a la subventana.
        self.horno_control.min_temp_entry = ttk.Entry(min_temp_frame)
        self.horno_control.min_temp_entry.insert(0, self.horno_control.min_temp)
        self.horno_control.min_temp_entry.pack(side=tk.TOP)

        # Crea un botón para actualizar la temperatura mínima y lo agrega a la subventana.
        self.horno_control.update_min_temp_button = ttk.Button(
            min_temp_frame, text="Actualizar Mínima", command=self.update_min_temp)
        self.horno_control.update_min_temp_button.pack(side=tk.TOP, pady=10)
        
        # Cambia el estado inicial de los otros botones a "disabled"
        self.horno_control.update_max_temp_button.configure(state='disabled')
        self.horno_control.update_min_temp_button.configure(state='disabled')
        
    def create_adquisition_button(self):
        # Crea un botón para Iniciar adquisición datos.
        self.horno_control.iniciar_adquisicion_button = ttk.Button(
        self.button_subframe, text="Iniciar adquisición datos", command=self.iniciar_adquisicion, state='normal')
        self.horno_control.iniciar_adquisicion_button.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N)
    
    def create_save_button(self):
        # Crea el botón de guardar los datos
        self.horno_control.save_button = ttk.Button(
            self.button_subframe, text="Guardar datos", command=self.exportar_datos_csv)
        self.horno_control.save_button.grid(row=2, column=0, padx=5, pady=5, sticky=tk.N)
        # Cambia el estado inicial de los otros botones a "disabled"
        self.horno_control.save_button.configure(state='disabled')
        
    def create_pause_button(self):
        # Crea el botón de pausa
        self.horno_control.pause_button = ttk.Button(
        self.button_subframe, text="Pausar", command=self.horno_control.toggle_pause)
        self.horno_control.pause_button.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N)     
        # Cambia el estado inicial de los otros botones a "disabled"
        self.horno_control.pause_button.configure(state='disabled')      
        
    def create_exit_button(self):
        # Crea un botón para salir de la aplicación y lo agrega a la ventana principal.
        self.horno_control.exitButton = ttk.Button(
            self.button_subframe, text="SALIR", command=self.confirm_exit)
        self.horno_control.exitButton.grid(row=7, column=0, padx=5, pady=5, sticky=tk.N)
        # Cambia el estado inicial de los otros botones a "disabled"
        # self.horno_control.exitButton.configure(state='disabled')
        
    def create_osciloscope_button(self):
        # Crea un botón para salir de la aplicación y lo agrega a la ventana principal.
        self.osciloscope = ttk.Button(
            self.button_subframe, text="Recogida Datos Osciloscopio", command=self.osc_autoconfiguration)
        self.osciloscope.grid(row=3, column=0, padx=5, pady=5, sticky=tk.N)
        # Cambia el estado inicial de los otros botones a "disabled"
        # self.horno_control.exitButton.configure(state='disabled')
        
    def create_multimeter_button(self):
        # Crea un botón para salir de la aplicación y lo agrega a la ventana principal.
        self.multimeter = ttk.Button(
            self.button_subframe, text="Recogida Datos Multímetro", command=self.mult_autoconfiguration)
        self.multimeter.grid(row=4, column=0, padx=5, pady=5, sticky=tk.N)
        # Cambia el estado inicial de los otros botones a "disabled"
        # self.horno_control.exitButton.configure(state='disabled')
        
    
    def create_DAQ_button(self):
        # Crea un botón para salir de la aplicación y lo agrega a la ventana principal.
        self.DAQ_button = ttk.Button(
            self.button_subframe, text="Recogida Datos DAQ", command=self.daq_autoconfiguration)
        self.DAQ_button.grid(row=5, column=0, padx=5, pady=5, sticky=tk.N)
        # Cambia el estado inicial de los otros botones a "disabled"
        # self.horno_control.exitButton.configure(state='disabled')
        
        
    def create_simulation_button(self):
        # Crea un botón para salir de la aplicación y lo agrega a la ventana principal.
        self.simulation_button = ttk.Button(
            self.button_subframe, text="Recogida Datos Simulados", command=self.simulation_autoconfiguration)
        self.simulation_button.grid(row=6, column=0, padx=5, pady=5, sticky=tk.N)
        # Cambia el estado inicial de los otros botones a "disabled"
        # self.horno_control.exitButton.configure(state='disabled')
        
    def create_button_subframe(self):
        # Crea un subframe para contener los botones
        self.button_subframe = ttk.Frame(self.subframe)
        self.button_subframe.grid(row=1, column=0, padx=5, pady=40, sticky=tk.N)
        self.button_subframe.rowconfigure(0, weight=1)
        self.button_subframe.columnconfigure(0, weight=1)
        self.create_exit_button()
        self.create_pause_button()
        self.create_save_button()
        self.create_adquisition_button()
        self.create_multimeter_button()
        self.create_osciloscope_button()
        self.create_DAQ_button()
        self.create_simulation_button()
        
    def create_subframe_gen(self):
        self.subframe = ttk.Frame(self.horno_control.root)
        self.subframe.grid(row=0, column=1, padx=5, pady=5, sticky=tk.E+tk.N)
        self.create_button_subframe()
        self.create_temperature_frame()
        self.subframe.rowconfigure(0, weight=5)
        self.subframe.columnconfigure(0, weight=5)
        
       
    def create_animation(self, fig: Figure):
        # Crea una animación para actualizar la gráfica de temperatura en tiempo real.
        self.horno_control.ani = animation.FuncAnimation(
            fig, self.grafica_real_time, interval=500)
        self.horno_control.ani_running = self.horno_control.canvas.get_tk_widget().after(
            0, self.horno_control.ani.event_source.start)
        
    
    def grafica_real_time(self, i: int):
        """
        Actualiza la gráfica de temperatura en tiempo real.
    
        Args:
            i (int): El número de veces que se ha llamado a la función.
        """
        # Esto está fuera de todos los if porque da igual el estado, siempre se debe mostrar
        self.update_current_temp()
        if self.horno_control.started and not self.horno_control.paused:
            self.horno_control.pause_button.config(text="Pausar")
            self.horno_control.count += 1
            self.update_temperature_data()
            self.update_temperature_graph()
            self.check_temperature_range()
        else:
            self.horno_control.pause_button.config(text="Reanudar")
    
    def update_temperature_data(self):
        """Actualiza los datos de temperatura."""
        self.update_act_temp()
        self.horno_control.x.append(self.horno_control.count * 0.5)
        self.horno_control.y1.append(self.horno_control.tempG)
        self.horno_control.y2.append(self.horno_control.max_temp)
        self.horno_control.y3.append(self.horno_control.min_temp)
        print(f"Tiempo: {self.horno_control.count * 0.5:.2f}s, Temperatura {self.horno_control.tempG:.2f}")
    
    def update_temperature_graph(self):
        """Actualiza la gráfica de temperatura."""
        self.ax.clear()
        self.ax.plot(self.horno_control.x, self.horno_control.y1, label='Temperatura')
        self.ax.plot(self.horno_control.x, self.horno_control.y2, label='Temp. Máx')
        self.ax.plot(self.horno_control.x, self.horno_control.y3, label='Temp. Mín')
        self.ax.legend(loc='best')
        self.ax.set_xlabel('Tiempo (s)')
        self.ax.set_ylabel('Temperatura (°C)')
    
    def check_temperature_range(self):
        """Verifica si la temperatura está dentro del rango establecido."""
        if self.horno_control.max_temp < self.horno_control.tempG:
            print("Estamos calientes")
            self.horno_daq.warm_state()
    
        elif self.horno_control.tempG < self.horno_control.min_temp:
            print("Estamos frios")
            self.horno_daq.cold_state()
        else:
            print("tamo bien")
            self.horno_daq.mild_state()
    
    def update_max_temp(self):
        """
        Actualiza la temperatura máxima con el valor ingresado por el usuario.
        """
        try:
            temp_str = self.horno_control.max_temp_entry.get()
            if temp_str:
                temp = float(temp_str)
                if self.is_valid_temperature(self.horno_control.min_temp, temp):
                    self.horno_control.max_temp = temp
                else:
                    tk.messagebox.showerror("Error", "La temperatura máxima no puede ser menor o igual a la temperatura mínima.")
            self.horno_control.max_temp_entry.delete(0, tk.END)
            self.horno_control.max_temp_entry.insert(0, self.horno_control.max_temp)
        except ValueError:
            tk.messagebox.showerror("Error", "Por favor, ingrese un número válido para la temperatura máxima")
    
    def update_min_temp(self):
        """
        Actualiza la temperatura mínima con el valor ingresado por el usuario.
        """
        try:
            temp_str = self.horno_control.min_temp_entry.get()
            if temp_str:
                temp = float(temp_str)
                if self.is_valid_temperature(temp, self.horno_control.max_temp):
                    self.horno_control.min_temp = temp
                else:
                    tk.messagebox.showerror("Error", "La temperatura mínima no puede ser mayor o igual a la temperatura máxima.")
            self.horno_control.min_temp_entry.delete(0, tk.END)
            self.horno_control.min_temp_entry.insert(0, self.horno_control.min_temp)
        except ValueError:
            tk.messagebox.showerror("Error", "Por favor, ingrese un número válido para la temperatura mínima")
    
    def update_act_temp(self):       
        if self.instrumento == Instrumentos.DAQ:
            try:
                self.horno_control.tempG = self.horno_daq.transform_voltage_temp()
            except:    
                self.horno_control.device_name = None
                self.start_check_thread()
        elif self.instrumento == Instrumentos.OSCILOSCOPIO:
            osc = HornoOsciloscopio.visa_resource(self)
            if osc is not None:    
                self.horno_control.tempG = HornoOsciloscopio.get_osc_voltage(self, osc)
            else:
                tk.messagebox.showerror("Error", "No se ha podido conectar a osciloscopio")
                self.instrumento = Instrumentos.DAQ
        elif self.instrumento == Instrumentos.MULTIMETRO:
            mult = HornoMultimetro.visa_resource(self)
            if mult is not None:
                self.horno_control.tempG = HornoMultimetro.get_mult_voltage(self, mult)
            else:
                self.instrumento = Instrumentos.DAQ
                tk.messagebox.showerror("Error", "No se ha podido conectar a multímetro")
        elif self.instrumento == Instrumentos.SIMULATION:
            self.horno_control.tempG = self.horno_daq.random_number_between_20_and_40(self.horno_control.tempG, 0)
        else:
            raise ValueError("Instrumento no válido")
        return self.horno_control.tempG
    
    def update_current_temp(self):
        """Define una función que actualice el valor de la etiqueta de temperatura actual."""
        temp = self.update_act_temp()
        self.horno_control.current_temp_var.set("{:.2f} ºC".format(temp))
    
    def exportar_datos_csv(self):
        """
        Exporta los datos de la medición en un archivo CSV.
        
        Primero, abre un diálogo para seleccionar la ruta y el nombre del archivo. Luego,
        escribe los datos en el archivo CSV.
        """
        # Obtener los datos a exportar
        x = self.horno_control.x
        y1 = self.horno_control.y1
        y2 = self.horno_control.y2
        y3 = self.horno_control.y3
        
        # Abrir un cuadro de diálogo para seleccionar la ruta y el nombre del archivo
        nombre_archivo = tk.filedialog.asksaveasfilename(defaultextension=".csv")
        if nombre_archivo:
            # Escribir los datos en el archivo CSV
            with open(nombre_archivo, 'w', newline='') as archivo_csv:
                writer = csv.writer(archivo_csv)
                writer.writerow(["Tiempo (s)", "Temperatura (°C)", "Temp. Máx (°C)", "Temp. Mín (°C)"])
                for i in range(len(x)):
                    writer.writerow([x[i], y1[i], y2[i], y3[i]])
            print("Datos exportados exitosamente.")
    
    def iniciar_adquisicion(self):
        """
        Inicia la adquisición de datos y actualiza el estado de los botones de la interfaz.
        """
        self.horno_control.iniciar_adquisicion_button.configure(state='disabled')
        self.horno_control.exitButton.configure(state='normal')
        self.horno_control.save_button.configure(state='normal')
        self.horno_control.pause_button.configure(state='normal')
        self.horno_control.update_max_temp_button.configure(state='normal')
        self.horno_control.update_min_temp_button.configure(state='normal')
        self.horno_control.toggle_start()
        self.horno_control.toggle_pause()
        
        
    def is_valid_temperature(self, new_min_temp: float, new_max_temp: float) -> bool:
        """
        Verifica si el rango de temperatura ingresado es válido.
        
        Args:
            new_min_temp (float): La nueva temperatura mínima propuesta.
            new_max_temp (float): La nueva temperatura máxima propuesta.
            
        Returns:
            bool: True si el rango es válido, False en caso contrario.
        """
        return new_min_temp < new_max_temp
        
    def start(self):
        """
        Inicia la interfaz gráfica de usuario (GUI).
        """
        self.setup_gui()
        tk.mainloop()
        
    def confirm_exit(self):
        # Muestra una pantalla de confirmación antes de salir
        confirm = tkinter.messagebox.askyesno("Confirmación", "¿Estás seguro de que quieres salir?")
        if confirm:
            self.horno_control.root.destroy()
        
        
    def mult_autoconfiguration(self):
        self.instrumento = Instrumentos.MULTIMETRO
        
    def osc_autoconfiguration(self):
        self.instrumento = Instrumentos.OSCILOSCOPIO
        tkinter.messagebox.showinfo("Menú de aviso", "Por favor, conecte el CH2 del osciloscopio a tierra")
        
    def daq_autoconfiguration(self):
         self.instrumento = Instrumentos.DAQ 
         
    def simulation_autoconfiguration(self):
        self.instrumento = Instrumentos.SIMULATION
        
    def check_device_name(self):
        while self.horno_control.device_name is None:
            self.horno_control.device_name = daq.get_connected_device()
            time.sleep(0.1)
        # self.update_voltage_label()
        
   
    # Hilos
    def start_check_thread(self):
        if not hasattr(self, 'check_thread') or not self.check_thread.is_alive():
            print("Entro al hilo")
            self.check_thread = threading.Thread(target=self.check_device_name)
            self.check_thread.daemon = True  # Hilo se ejecutará en segundo plano idealmente
            self.check_thread.start()
        else:
            print("El hilo ya está en ejecución")

    
